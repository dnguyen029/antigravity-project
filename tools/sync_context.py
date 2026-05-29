import os
import json
import asyncio
import requests
import datetime

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

async def _save_memory_mcp(proc, content):
    try:
        # Step 1: Initialize handshake
        init_req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "sync-context-cli", "version": "1.0.0"}
            }
        }
        proc.stdin.write((json.dumps(init_req) + "\n").encode("utf-8"))
        await proc.stdin.drain()

        # Read initialize response
        init_res = await read_json_rpc(proc.stdout, 1)
        if not init_res:
            return False, "Error: MCP initialization handshake failed."

        # Step 2: Request tool call
        call_req = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "memory",
                "arguments": {
                    "action": "save",
                    "content": content
                }
            }
        }
        proc.stdin.write((json.dumps(call_req) + "\n").encode("utf-8"))
        await proc.stdin.drain()

        # Read response
        response_data = await read_json_rpc(proc.stdout, 2)
        if response_data and "result" in response_data:
            return True, response_data["result"]
        elif response_data and "error" in response_data:
            return False, f"Error from Supermemory: {response_data['error']}"
        return False, "Failed to get response from Supermemory."
    except Exception as e:
        return False, f"Error during query execution: {e}"

async def sync_to_supermemory(content):
    """Pushes memory content to Supermemory MCP server."""
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
        success, result = await asyncio.wait_for(_save_memory_mcp(proc, content), timeout=25.0)
        if success:
            return f"Success: {result}"
        else:
            return f"Failure: {result}"
    except asyncio.TimeoutError:
        return "Error: Supermemory connection timed out."
    finally:
        if proc:
            try:
                proc.kill()
                await proc.wait()
            except:
                pass

def get_supabase_lessons(limit=10):
    """Queries Supabase directly via REST API for the latest lessons learned."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL or SUPABASE_KEY missing in environment.")

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    res = requests.get(
        f"{url}/rest/v1/lessons_learned?select=*&order=created_at.desc&limit={limit}",
        headers=headers,
        timeout=15
    )
    if res.status_code != 200:
        raise RuntimeError(f"Error querying Supabase: Status {res.status_code} - {res.text}")
    
    return res.json()

async def main():
    print("="*60)
    print("SYNCHRONIZING SUPABASE LESSONS TO SUPERMEMORY")
    print("="*60)
    
    try:
        print("[1] Fetching latest 10 lessons from Supabase...")
        lessons = get_supabase_lessons(limit=10)
        if not lessons:
            print("No lessons found in Supabase to sync.")
            return

        print(f"Found {len(lessons)} lessons.")
        
        # Build a consolidated markdown block of findings/lessons to push to Supermemory
        sync_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        content_parts = [
            f"=== SUPABASE LESSONS SYNCED ON {sync_time} ==="
        ]
        
        for idx, rec in enumerate(lessons, 1):
            topic = rec.get("topic", "N/A")
            created_at = rec.get("created_at", "N/A")
            content = rec.get("content", "N/A")
            agent = rec.get("agent", "N/A")
            tags = ", ".join(rec.get("tags", [])) if rec.get("tags") else "None"
            
            content_parts.append(
                f"{idx}. **Topic**: {topic}\n"
                f"   **Agent**: {agent} | **Date**: {created_at} | **Tags**: {tags}\n"
                f"   **Content**: {content}\n"
            )
            
        consolidated_content = "\n".join(content_parts)
        
        print("\n[2] Pushing consolidated lessons to Supermemory...")
        result = await sync_to_supermemory(consolidated_content)
        print("-" * 60)
        print(result)
        print("-" * 60)
        
    except Exception as e:
        print(f"Sync failed with error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
