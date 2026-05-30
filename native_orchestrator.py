"""
================================================================================
🏛️ NATIVE ANTIGRAVITY 2.0 SDK ORCHESTRATION BLUEPRINT
================================================================================

This module implements the execution and governance engine for the Antigravity
Swarm using the native google-antigravity SDK. It coordinates lifecycle states,
enforces permission boundaries via hooks, and leverages workspace capabilities.
"""

import os
import sys
import json
import logging
import asyncio
from google.antigravity import Agent, LocalAgentConfig, types
from google.antigravity.hooks import policy

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("native_orchestrator")

def load_env():
    """Load env variables from .env if present."""
    env_path = ".env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and "=" in stripped:
                    key, val = stripped.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env()

def load_mcp_servers(agent_role: str = None):
    """Load and parse workspace MCP servers."""
    mcp_servers = []
    config_path = "mcp_config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"{config_path} is missing. Cannot verify MCP configurations.")
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    servers = config.get("mcpServers", {})
    
    # Enforce mandatory Supabase registry connection to protect the database layer
    if "supabase" not in servers:
        raise ValueError("Mandatory 'supabase' server configuration is missing from mcp_config.json.")
        
    for name, srv in servers.items():
        if "url" in srv or "serverURL" in srv:
            url = srv.get("url") or srv.get("serverURL")
            headers = srv.get("headers")
            if "supabase" in name or "supabase.com" in url:
                if not headers or "Authorization" not in headers or not headers.get("Authorization"):
                    raise ValueError(f"Mandatory '{name}' (Supabase) is missing a valid Authorization header.")
            mcp_servers.append(types.McpSseServer(url=url, headers=headers))
        else:
            mcp_servers.append(types.McpStdioServer(
                command=srv.get("command"),
                args=srv.get("args", []),
                env=srv.get("env")
            ))
    return mcp_servers

def get_policies_for_role(agent_role: str):
    """Native SDK Safety Hook & Quartet Policy Guard.
    Validates execution boundaries and directory protections dynamically using native Policy objects.
    """
    role_lower = agent_role.lower()
    
    # 1. Prohibited Directories (Access Protection)
    prohibited_folders = [".venv", ".git", "venv", "node_modules"]
    
    def contains_prohibited_folder(args):
        paths_to_check = [
            args.get(k) for k in ["path", "AbsolutePath", "DirectoryPath", "TargetFile", "SearchPath"]
            if k in args and isinstance(args[k], str)
        ]
        for file_path in paths_to_check:
            normalized_path = file_path.replace("\\", "/")
            parts = normalized_path.split("/")
            if any(folder in parts for folder in prohibited_folders):
                return True
        return False

    # 2. Token-Waste Prevention
    def is_broad_search(args):
        path_arg = args.get("SearchPath") or args.get("DirectoryPath") or ""
        if path_arg in ["/", "/home/dnguyen029/antigravity-project", "/home/dnguyen029/antigravity-project/"]:
            if args.get("Query") in ["", "*", ".*"]:
                return True
        return False

    # 3. Write Constraints & Document Debt Prevention
    def is_writing_without_plan(args):
        target_file = args.get("TargetFile") or args.get("file_path") or args.get("path") or ""
        target_basename = os.path.basename(target_file)
        if target_basename in ["implementation_plan.md", "task.md", "walkthrough.md"]:
            return False
        plan_file = "implementation_plan.md"
        if not os.path.exists(plan_file):
            return True
        with open(plan_file, "r") as f:
            content = f.read()
            if "## Proposed Changes" not in content and "## Root Cause Analysis" not in content:
                return True
        return False

    policies = [
        policy.deny("*", when=contains_prohibited_folder, name="prohibited_folders"),
        policy.deny("grep_search", when=is_broad_search, name="token_waste_grep"),
        policy.deny("list_dir", when=is_broad_search, name="token_waste_list_dir"),
    ]

    write_tools = ["write_file", "edit_file", "write_to_file", "replace_file_content", "multi_replace_file_content", "delete_file"]
    for wt in write_tools:
        policies.append(policy.deny(wt, when=is_writing_without_plan, name=f"write_guard_{wt}"))

    # 4. Role-Based Quartet Permission Check
    if "orchestrator" in role_lower or "architect" in role_lower:
        def is_not_planning_file(args):
            target_file = args.get("TargetFile") or args.get("file_path") or args.get("path") or ""
            return os.path.basename(target_file) not in ["implementation_plan.md", "task.md", "walkthrough.md"]
            
        for wt in write_tools:
            policies.append(policy.deny(wt, when=is_not_planning_file, name=f"orchestrator_write_restrict_{wt}"))
        policies.append(policy.deny("run_command", name="orchestrator_deny_run_command"))
        policies.append(policy.deny("execute_command", name="orchestrator_deny_exec_command"))

    elif "auditor" in role_lower:
        for wt in write_tools:
            policies.append(policy.deny(wt, name=f"auditor_deny_write_{wt}"))
        policies.append(policy.deny("run_command", name="auditor_deny_run_command"))
        policies.append(policy.deny("execute_command", name="auditor_deny_exec_command"))

    elif "librarian" in role_lower or "writer" in role_lower:
        def is_code_config_file(args):
            target_file = args.get("TargetFile") or args.get("file_path") or args.get("path") or ""
            _, ext = os.path.splitext(os.path.basename(target_file))
            return ext.lower() in [".py", ".json", ".env", ".yaml", ".yml"]
            
        for wt in write_tools:
            policies.append(policy.deny(wt, when=is_code_config_file, name=f"librarian_deny_code_write_{wt}"))

    elif "builder" in role_lower or "developer" in role_lower or "admin" in role_lower or "sre" in role_lower:
        policies.append(policy.deny("memory", name="builder_deny_memory"))
        policies.append(policy.deny("apply_migration", name="builder_deny_migration"))
        
        def is_modifying_sql(args):
            query = args.get("query", "").strip().upper()
            write_keywords = ["INSERT ", "UPDATE ", "DELETE ", "DROP ", "CREATE ", "ALTER ", "REPLACE ", "TRUNCATE "]
            return any(kw in query for kw in write_keywords)
            
        policies.append(policy.deny("execute_sql", when=is_modifying_sql, name="builder_deny_write_sql"))

    # Approval handler for run_command / execute_command in dynamic/interactive/developer scenarios
    async def ask_user_handler(tool_call):
        print(f"\n❓ [APPROVAL REQUIRED] Agent '{agent_role}' wants to run: {tool_call.name}")
        if hasattr(tool_call, "arguments") and tool_call.arguments:
            print(f"Arguments: {json.dumps(tool_call.arguments, indent=2)}")
        user_input = await asyncio.to_thread(input, "Allow execution? (yes/no): ")
        return user_input.strip().lower() in ["yes", "y"]

    policies.append(policy.ask_user("run_command", handler=ask_user_handler, name="ask_run_command"))
    policies.append(policy.ask_user("execute_command", handler=ask_user_handler, name="ask_exec_command"))
    policies.append(policy.allow_all())
    
    return policies

class SwarmOrchestrator:
    def __init__(self, task_description: str):
        self.task_description = task_description
        self.plan_path = "implementation_plan.md"
        self.task_path = "task.md"
        self.walkthrough_path = "walkthrough.md"
        self.approved = False
        self.memory_context = ""

    async def execute_workflow(self):
        """Standardized async agent runner executing Discovery, Planning, and Verification stages."""
        logger.info("🔍 [PHASE 1: DISCOVERY] Initializing native workspace validation...")
        if not os.path.exists(".env"):
            raise FileNotFoundError("Missing environment credentials (.env file).")
            
        logger.info("📋 [PHASE 2: PLANNING] Querying Supermemory & Supabase database contexts...")
        if os.path.exists("instructions/librarian.txt"):
            with open("instructions/librarian.txt", "r") as f:
                librarian_instr = f.read()
            
            lib_config = LocalAgentConfig(
                system_instructions=librarian_instr,
                capabilities=types.CapabilitiesConfig(enable_subagents=True),
                policies=get_policies_for_role("librarian"),
                mcp_servers=load_mcp_servers("librarian"),
                max_turns=5
            )
            
            async with Agent(lib_config) as librarian:
                task_resp = await librarian.chat(
                    f"Search your databases for past resolutions/lessons about: \"{self.task_description}\"."
                )
                task_text = await task_resp.text()
                
                gen_resp = await librarian.chat(
                    "Search databases for general project architecture and swarm roles guidelines."
                )
                gen_text = await gen_resp.text()
                
                self.memory_context = f"=== TASK WISDOM ===\n{task_text}\n\n=== GENERAL GUIDELINES ===\n{gen_text}"

        logger.info("Writing implementation plan using Architect agent...")
        with open("instructions/architect.txt", "r") as f:
            arch_instr = f.read()
        if self.memory_context:
            arch_instr += f"\n\n## 🧠 RECALLED MISSION WISDOM\n{self.memory_context}"

        arch_config = LocalAgentConfig(
            system_instructions=arch_instr,
            capabilities=types.CapabilitiesConfig(enable_subagents=True),
            policies=get_policies_for_role("architect"),
            mcp_servers=load_mcp_servers("architect"),
            max_turns=5
        )
        async with Agent(arch_config) as architect:
            resp = await architect.chat(
                f"Draft an implementation plan and task lists for task: \"{self.task_description}\"."
            )
            plan_content = await resp.text()
            with open(self.plan_path, "w") as f:
                f.write(plan_content)
            
            if not os.path.exists(self.task_path):
                with open(self.task_path, "w") as f:
                    f.write("# Task Tracking\n\n- [ ] Task initialized.\n")

        # Approval Gate
        logger.info(f"🛑 [APPROVAL GATE] Please review {self.plan_path}.")
        user_input = await asyncio.to_thread(input, "Approve plan and authorize execution? (yes/no): ")
        if user_input.strip().lower() in ["yes", "y"]:
            self.approved = True
        else:
            logger.warning("Plan rejected. Halting execution.")
            return

        logger.info("💻 [PHASE 3: EXECUTION] Spawning Builder to implement code changes...")
        with open("instructions/builder.txt", "r") as f:
            build_instr = f.read()
        if self.memory_context:
            build_instr += f"\n\n## 🧠 RECALLED MISSION WISDOM\n{self.memory_context}"

        builder_config = LocalAgentConfig(
            system_instructions=build_instr,
            capabilities=types.CapabilitiesConfig(enable_subagents=True),
            policies=get_policies_for_role("builder"),
            mcp_servers=load_mcp_servers("builder"),
            max_turns=5
        )
        async with Agent(builder_config) as builder:
            exec_resp = await builder.chat(
                f"Execute changes outlined in '{self.plan_path}' and update status in '{self.task_path}'."
            )
            print(await exec_resp.text())

        # Compile validation
        logger.info("⚙️ [SYNTAX CHECK] Compiling Python files...")
        import glob
        import py_compile
        for file in glob.glob("*.py") + glob.glob("tools/*.py"):
            try:
                py_compile.compile(file, doraise=True)
            except py_compile.PyCompileError as e:
                logger.error(f"Syntax validation failed on: {file} - {e}")
                sys.exit(1)

        logger.info("🛡️ [PHASE 4: VERIFICATION] Spawning Librarian for final sync...")
        with open("instructions/librarian.txt", "r") as f:
            lib_instr = f.read()
        if self.memory_context:
            lib_instr += f"\n\n## 🧠 RECALLED MISSION WISDOM\n{self.memory_context}"

        lib_config = LocalAgentConfig(
            system_instructions=lib_instr,
            capabilities=types.CapabilitiesConfig(enable_subagents=True),
            policies=get_policies_for_role("librarian"),
            mcp_servers=load_mcp_servers("librarian"),
            max_turns=5
        )
        async with Agent(lib_config) as librarian:
            sync_resp = await librarian.chat(
                f"Verify changes, write '{self.walkthrough_path}', and sync state to Supabase."
            )
            print(await sync_resp.text())
        logger.info("🎉 Swarm execution workflow successfully completed!")

async def main():
    if len(sys.argv) < 2:
        print("Usage: python native_orchestrator.py \"<task description>\"")
        sys.exit(1)
    task = sys.argv[1]
    orchestrator = SwarmOrchestrator(task)
    await orchestrator.execute_workflow()

if __name__ == "__main__":
    asyncio.run(main())
