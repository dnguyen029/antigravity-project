import os
import json
import asyncio
import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("context-mcp")

def load_env():
    """Load env variables from .env if present."""
    env_path = "/home/dnguyen029/antigravity-project/.env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and "=" in stripped:
                    key, val = stripped.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env()

async def read_json_rpc(stdout, request_id=None):
    """Reads lines from stdout until a valid JSON-RPC message with target id is found."""
    while True:
        line_bytes = await stdout.readline()
        if not line_bytes:
            break
        line = line_bytes.decode("utf-8", errors="ignore").strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            if data.get("jsonrpc") == "2.0":
                if request_id is None or data.get("id") == request_id:
                    return data
        except json.JSONDecodeError:
            continue
    return None

async def _query_mcp_internal(proc):
    try:
        # Step 1: Initialize handshake
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "fetch-context-cli", "version": "1.0.0"}
            }
        }
        proc.stdin.write((json.dumps(init_req) + "\n").encode("utf-8"))
        await proc.stdin.drain()

        # Read initialize response
        init_res = await read_json_rpc(proc.stdout, 1)
        if not init_res:
            return "Error: MCP initialization handshake timed out or failed."

        # Step 2: Request resource read
        read_req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "resources/read",
            "params": {
                "uri": "supermemory://profile"
            }
        }
        proc.stdin.write((json.dumps(read_req) + "\n").encode("utf-8"))
        await proc.stdin.drain()

        # Read response
        response_data = await read_json_rpc(proc.stdout, 2)
        if response_data and "result" in response_data:
            contents = response_data["result"].get("contents", [])
            if contents:
                return contents[0].get("text", "No profile text returned.")
            return "No contents found in resource response."
        elif response_data and "error" in response_data:
            return f"Error from Supermemory: {response_data['error']}"
        return "Failed to get response from Supermemory."
    except Exception as e:
        return f"Error during query execution: {e}"

async def get_supermemory_profile():
    """Queries the Supermemory MCP server programmatically using robust JSON-RPC stdio connection."""
    config_path = "/home/dnguyen029/antigravity-project/mcp_config.json"
    if not os.path.exists(config_path):
        return "Error: mcp_config.json not found."

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        srv = config.get("mcpServers", {}).get("supermemory", {})
        if not srv:
            return "Error: supermemory configuration missing from mcp_config.json."
    except Exception as e:
        return f"Error reading config: {e}"

    command = srv.get("command", "npx")
    args = srv.get("args", [])
    
    # Start the MCP subprocess
    proc = None
    try:
        proc = await asyncio.create_subprocess_exec(
            command,
            *args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL
        )
    except FileNotFoundError:
        try:
            cmd_str = f"{command} " + " ".join([f'"{a}"' for a in args])
            proc = await asyncio.create_subprocess_shell(
                cmd_str,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL
            )
        except Exception as e:
            return f"Failed to start Supermemory process: {e}"
    except Exception as e:
        return f"Failed to start Supermemory process: {e}"

    try:
        # Run query with an overall 20-second timeout
        result = await asyncio.wait_for(_query_mcp_internal(proc), timeout=20.0)
        return result
    except asyncio.TimeoutError:
        return "Error: Supermemory connection timed out (overall 20-second limit reached)."
    finally:
        if proc:
            try:
                proc.kill()
                await asyncio.wait_for(proc.wait(), timeout=2.0)
            except:
                pass

def get_supabase_lessons():
    """Queries Supabase directly via REST API for the latest lessons learned."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        return "Error: SUPABASE_URL or SUPABASE_KEY missing in environment."

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    try:
        res = requests.get(
            f"{url}/rest/v1/lessons_learned?select=*&order=created_at.desc&limit=5",
            headers=headers,
            timeout=10
        )
        if res.status_code != 200:
            return f"Error querying Supabase: Status {res.status_code} - {res.text}"
        
        records = res.json()
        output = []
        for rec in records:
            topic = rec.get("topic", "N/A")
            created_at = rec.get("created_at", "N/A")
            content = rec.get("content", "N/A")
            agent = rec.get("agent", "N/A")
            output.append(f"- **Topic**: {topic}\n  **Agent**: {agent} | **Date**: {created_at}\n  **Content**: {content}\n")
        return "\n".join(output) if output else "No lessons found."
    except Exception as e:
        return f"Exception querying Supabase: {e}"

@mcp.prompt()
async def lessons() -> str:
    """Retrieve user profile from Supermemory and latest lessons from Supabase."""
    sm_profile = await get_supermemory_profile()
    sb_lessons = get_supabase_lessons()
    
    return f"""=== USER PROFILE & STABLE CONTEXT ===
{sm_profile}

=== LATEST LESSONS LEARNED ===
{sb_lessons}
"""

if __name__ == "__main__":
    mcp.run()
