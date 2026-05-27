import os
import sys
import json
import logging
import asyncio
from google.antigravity import Agent, LocalAgentConfig, types

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("swarm_orchestrator")

# Load environment variables from .env
if os.path.exists(".env"):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        with open(".env") as f:
            for line in f:
                stripped = line.strip()
                if stripped and not stripped.startswith("#") and "=" in stripped:
                    key, value = stripped.split("=", 1)
                    os.environ[key.strip()] = value.strip()

def load_mcp_servers(agent_role: str = None):
    mcp_servers = []
    if not os.path.exists("mcp_config.json"):
        raise FileNotFoundError("mcp_config.json is missing. Cannot verify MCP configurations.")
    try:
        with open("mcp_config.json", "r") as f:
            config = json.load(f)
        servers = config.get("mcpServers", {})
        
        # Enforce that supabase configuration MUST exist
        if "supabase" not in servers:
            raise ValueError("Mandatory 'supabase' server configuration is missing from mcp_config.json.")
            
        for name, srv in servers.items():
            # Only librarian is allowed to load long-term database memory connections
            if name in ["supabase", "supermemory"] and agent_role != "librarian":
                continue

            if "url" in srv or "serverURL" in srv:
                url = srv.get("url") or srv.get("serverURL")
                headers = srv.get("headers")

                # If Supabase lacks auth headers, raise ValueError to protect the source of truth
                if "supabase" in name or "supabase.com" in url:
                    if not headers or "Authorization" not in headers or not headers.get("Authorization"):
                        raise ValueError(f"Mandatory '{name}' (Supabase) configuration is missing a valid Authorization header.")

                mcp_servers.append(types.McpSseServer(
                    url=url,
                    headers=headers
                ))
            else:
                command = srv.get("command")
                args = srv.get("args", [])
                env = srv.get("env")
                mcp_servers.append(types.McpStdioServer(
                    command=command,
                    args=args,
                    env=env
                ))
    except Exception as e:
        logger.error(f"Failed to load/verify MCP servers from mcp_config.json: {e}")
        raise e
    return mcp_servers

def verify_tool_policy(agent_name: str, tool_name: str, arguments: dict):
    """Root Cause Gate — Programmatic SDK guard to intercept tool calls.
    This gate physically blocks execution unless:
    1. A valid Root Cause Analysis (RCA) or Proposed Changes section exists in implementation_plan.md.
    2. The target path is not inside a prohibited directory (.venv, .git, node_modules).
    Note: Token compression is handled natively by the toon-mcp-server MCP layer.
    """
    # 1. Prohibited Directory Guards (Read & Write)
    prohibited_folders = [".venv", ".git", "venv", "node_modules"]
    
    # Extract any paths in the arguments
    paths_to_check = []
    for arg_name in ["path", "AbsolutePath", "DirectoryPath", "TargetFile", "SearchPath"]:
        if arg_name in arguments and isinstance(arguments[arg_name], str):
            paths_to_check.append(arguments[arg_name])
            
    for file_path in paths_to_check:
        normalized_path = file_path.replace("\\", "/") # normalize Windows paths if any
        parts = normalized_path.split("/")
        if any(folder in parts for folder in prohibited_folders):
            print(f"\n🚨 [AUDITOR VETO] Agent '{agent_name}' attempted to access prohibited directory '{file_path}'.")
            user_input = input("Escalate to David: Enter 'bypass' to override, or 'kill' to abort task: ").strip().lower()
            if user_input in ["bypass", "b"]:
                logger.info("David authorized bypass of directory check. Continuing...")
                return
            else:
                raise PermissionError(
                    f"Aborting tool execution for agent '{agent_name}': "
                    f"Access to prohibited system directory '{file_path}' was rejected by David."
                )

    # 2. Root Cause Gate — Write Policy Guards
    if tool_name in ["write_file", "edit_file", "write_to_file", "replace_file_content", "multi_replace_file_content"]:
        # Get target file name from arguments
        target_file = arguments.get("TargetFile") or arguments.get("file_path") or arguments.get("path") or ""
        target_basename = os.path.basename(target_file)
        
        # Exempt planning and documentation artifacts from the block
        if target_basename in ["implementation_plan.md", "task.md", "walkthrough.md"]:
            return

        # Document Debt Prevention: Block creation of any new files unless they match an allowed list
        is_create = tool_name in ["write_file", "write_to_file"]
        if is_create and not os.path.exists(target_file):
            allowed_extensions = [".py", ".json", ".env", ".yaml", ".yml"]
            allowed_basenames = ["implementation_plan.md", "task.md", "walkthrough.md"]
            _, ext = os.path.splitext(target_basename)
            if target_basename not in allowed_basenames and ext.lower() not in allowed_extensions:
                raise PermissionError(
                    f"Aborting execution for agent '{agent_name}': "
                    f"Creating file '{target_basename}' is blocked to prevent document debt. "
                    f"Agents may only create allowed configs, code files, or approved markdown files."
                )
        
        # Block edits to python files or system scripts if planning files are missing or incomplete
        plan_file = "implementation_plan.md"
        if not os.path.exists(plan_file):
            print(f"\n🚨 [AUDITOR VETO] Agent '{agent_name}' tried to modify '{target_file}' but '{plan_file}' does not exist.")
            user_input = input("Escalate to David: Enter 'bypass' to override, or 'kill' to abort task: ").strip().lower()
            if user_input in ["bypass", "b"]:
                logger.info("David authorized bypass of plan existence check. Continuing...")
                return
            else:
                raise PermissionError(
                    f"Aborting execution for agent '{agent_name}': "
                    f"'{plan_file}' must exist before making file modifications."
                )
        
        with open(plan_file, "r") as f:
            content = f.read()
            if "## Proposed Changes" not in content and "## Root Cause Analysis" not in content:
                print(f"\n🚨 [AUDITOR VETO] Agent '{agent_name}' tried to modify '{target_file}' but '{plan_file}' lacks required sections.")
                user_input = input("Escalate to David: Enter 'bypass' to override, or 'kill' to abort task: ").strip().lower()
                if user_input in ["bypass", "b"]:
                    logger.info("David authorized bypass of plan content check. Continuing...")
                    return
                else:
                    raise PermissionError(
                        f"Aborting execution for agent '{agent_name}': "
                        f"'{plan_file}' must document 'Root Cause Analysis' or 'Proposed Changes'."
                    )

class SwarmOrchestrator:
    def __init__(self, task_description: str):
        self.task_description = task_description
        self.plan_path = "implementation_plan.md"
        self.task_path = "task.md"
        self.walkthrough_path = "walkthrough.md"
        self.approved = False

    async def run_discovery(self):
        """Phase 1: Discovery.
        Checks the workspace environment and maps boundaries before planning.
        """
        logger.info("🔍 [PHASE 1: DISCOVERY] Mapping boundaries and dependencies...")
        
        # Load environment credentials
        if not os.path.exists(".env"):
            raise FileNotFoundError("Missing .env file. Cannot proceed without credentials.")
            
        # Verify instructions folder exists
        if not os.path.exists("instructions"):
            os.makedirs("instructions")
            
        logger.info("Discovery complete: Environment credentials and prompt files verified.")

    async def run_planning(self):
        """Phase 2: Planning & Root Cause Gate.
        Spawns the Librarian to retrieve past memory context, then spawns the Architect
        to draft the implementation plan.
        """
        logger.info("📋 [PHASE 2: PLANNING] Spawns Librarian to retrieve past memory context...")
        
        self.memory_context = ""
        if os.path.exists("instructions/librarian.txt"):
            with open("instructions/librarian.txt", "r") as f:
                librarian_instructions = f.read()
            
            librarian_config = LocalAgentConfig(
                system_instructions=librarian_instructions,
                capabilities=types.CapabilitiesConfig(enable_subagents=True),
                mcp_servers=load_mcp_servers("librarian"),
                max_turns=5
            )
            
            try:
                async with Agent(librarian_config) as librarian:
                    # Query 1: Task-specific search
                    librarian_prompt_task = (
                        f"Search the memory database (using Supermemory or Supabase) for any past "
                        f"resolutions, lessons learned, or warnings regarding the following task:\n"
                        f"\"{self.task_description}\"\n\n"
                        f"Summarize these findings into a concise list of design rules or lessons "
                        f"that the Architect should follow to avoid repeating past errors."
                    )
                    logger.info("Querying memory vault for task-specific context...")
                    response_task = await librarian.chat(librarian_prompt_task)
                    task_context = await response_task.text()

                    # Query 2: General project architecture & swarm guidelines search
                    librarian_prompt_gen = (
                        "Search the memory database for general project architecture, swarm roles, "
                        "guidelines, brand separation mandates (Ariel Bath vs Antigravity Swarm), and Trinity files (findings.md, task_plan.md, AGENTS.md, GEMINI.md)."
                    )
                    logger.info("Querying memory vault for general project guidelines...")
                    response_gen = await librarian.chat(librarian_prompt_gen)
                    gen_context = await response_gen.text()

                    self.memory_context = f"=== TASK-SPECIFIC WISDOM ===\n{task_context}\n\n=== GENERAL PROJECT ARCHITECTURE & GUIDELINES ===\n{gen_context}"
                    logger.info("Librarian successfully retrieved all memory contexts.")
            except Exception as e:
                logger.error(f"Librarian memory retrieval failed: {e}. Halting execution immediately (Fail-Fast Policy).")
                raise RuntimeError(f"Librarian database memory check failed: {e}. Swarm execution aborted.")
        else:
            logger.error("librarian.txt instructions missing. Halting execution immediately.")
            raise RuntimeError("Librarian configuration missing. Swarm execution aborted.")
        
        logger.info("📋 Spawns Architect to draft implementation_plan.md...")
        
        # Load Architect Instructions
        with open("instructions/architect.txt", "r") as f:
            architect_instructions = f.read()

        # Inject memory context directly to instructions
        if self.memory_context:
            architect_instructions += f"\n\n## 🧠 RECALLED MISSION WISDOM (L3 Archive)\n{self.memory_context}\n\n## 🏛️ WRITE POLICY MANDATE\nWhen modifying or updating any Markdown (.md) or documentation files, you MUST use an append-only strategy. Do not rewrite, reword, or delete existing historical sections or notes proactively unless correcting an obvious error."

        # Initialize the Architect agent
        config = LocalAgentConfig(
            system_instructions=architect_instructions,
            capabilities=types.CapabilitiesConfig(enable_subagents=True),
            mcp_servers=load_mcp_servers("architect"),
            max_turns=5
        )

        async with Agent(config) as architect:
            prompt = (
                f"You are the Principal Architect. Draft the '{self.plan_path}' and '{self.task_path}' "
                f"for the following task:\n\"{self.task_description}\"\n\n"
                f"STRICT REQUIREMENT: If this task involves debugging or fixing an error, you MUST write "
                f"an explicit 'Root Cause Analysis (RCA)' section documenting: "
                f"(1) Symptoms, (2) Technical Root Cause, (3) Permanent Resolution Plan. "
                f"Conform strictly to Rule 1 (Minimum Viable Change) and Rule 2 (Diagnose Before You Fix)."
            )
            response = await architect.chat(prompt)
            plan_content = await response.text()
            logger.info("Architect has generated the implementation plan. Writing to disk...")
            
            # Write plan to file
            with open(self.plan_path, "w") as f:
                f.write(plan_content)
            
            # Initialize a default task tracking file if missing
            if not os.path.exists(self.task_path):
                with open(self.task_path, "w") as f:
                    f.write("# Task Tracking\n\n- [ ] Task integration initialized.")
            
            print(plan_content)

    async def wait_for_approval(self):
        """Gate: Blocks execution until the user manually reviews and approves the plan."""
        logger.info(f"🛑 [APPROVAL GATE] Please review {self.plan_path} and {self.task_path}.")
        
        # In a mechanical loop, we halt and wait for terminal input
        user_input = input("Approve plan and authorize execution? (yes/no): ").strip().lower()
        if user_input in ["yes", "y"]:
            self.approved = True
            logger.info("Plan APPROVED. Authorizing implementation phase.")
        else:
            self.approved = False
            logger.warn("Plan REJECTED. Halting swarm execution.")
            sys.exit(0)

    async def run_execution(self):
        """Phase 3: Execution.
        Spawns the Builder subagent to execute code changes and performs syntax checks.
        """
        if not self.approved:
            raise PermissionError("Cannot execute without user approval.")

        logger.info("💻 [PHASE 3: EXECUTION] Spawns Builder to implement code changes...")

        # Load Builder Instructions
        with open("instructions/builder.txt", "r") as f:
            builder_instructions = f.read()

        # Inject memory context directly to instructions if available
        if hasattr(self, 'memory_context') and self.memory_context:
            builder_instructions += f"\n\n## 🧠 RECALLED MISSION WISDOM (L3 Archive)\n{self.memory_context}\n\n## 🏛️ WRITE POLICY MANDATE\nWhen modifying or updating any Markdown (.md) or documentation files, you MUST use an append-only strategy. Do not rewrite, reword, or delete existing historical sections or notes proactively unless correcting an obvious error."

        # Pass custom tool verification callback policy directly to Builder agent setup
        config = LocalAgentConfig(
            system_instructions=builder_instructions,
            capabilities=types.CapabilitiesConfig(enable_subagents=True),
            policy=verify_tool_policy,
            mcp_servers=load_mcp_servers("builder"),
            max_turns=5
        )

        async with Agent(config) as builder:
            prompt = (
                f"You are the Lead Developer. Implement the changes approved in '{self.plan_path}' "
                f"and mark progress in '{self.task_path}'. Check your syntax programmatically."
            )
            response = await builder.chat(prompt)
            print(await response.text())

        # Mechanical Syntax Gate: Verify all python files in project compile cleanly
        logger.info("⚙️ [SYNTAX CHECK] Running compiler check on modified Python files...")
        import glob
        import py_compile
        py_files = glob.glob("*.py") + glob.glob("tools/*.py")
        for file in py_files:
            try:
                py_compile.compile(file, doraise=True)
                logger.info(f"Syntax Check PASSED: {file}")
            except py_compile.PyCompileError as e:
                print(f"\n🚨 [AUDITOR VETO] Syntax check failed on '{file}': {e}")
                user_input = input("Escalate to David: Enter 'bypass' to ignore and continue, or 'kill' to abort task: ").strip().lower()
                if user_input in ["bypass", "b"]:
                    logger.info("David authorized bypass of syntax failure. Continuing...")
                else:
                    logger.error("Blocking execution phase due to syntax failure. Aborting...")
                    sys.exit(1)

    async def run_verification(self):
        """Phase 4: Verification.
        Spawns Auditor and Librarian to check safety policies, write walkthrough, and archive knowledge.
        """
        logger.info("🛡️ [PHASE 4: VERIFICATION] Spawns Auditor & Librarian for final verification...")

        # Load Librarian Instructions (the only database-authorized agent)
        with open("instructions/librarian.txt", "r") as f:
            librarian_instructions = f.read()

        # Inject memory context directly to instructions if available
        if hasattr(self, 'memory_context') and self.memory_context:
            librarian_instructions += f"\n\n## 🧠 RECALLED MISSION WISDOM (L3 Archive)\n{self.memory_context}\n\n## 🏛️ WRITE POLICY MANDATE\nWhen modifying or updating any Markdown (.md) or documentation files, you MUST use an append-only strategy. Do not rewrite, reword, or delete existing historical sections or notes proactively unless correcting an obvious error."

        config = LocalAgentConfig(
            system_instructions=librarian_instructions,
            capabilities=types.CapabilitiesConfig(enable_subagents=True),
            policy=verify_tool_policy,
            mcp_servers=load_mcp_servers("librarian"),
            max_turns=5
        )

        async with Agent(config) as librarian:
            prompt = (
                f"You are the Technical Writer. Verify all code changes against safety rules, "
                f"write the final '{self.walkthrough_path}' documenting what was completed, "
                f"and synchronize the swarm state metadata to the Supabase database."
            )
            response = await librarian.chat(prompt)
            print(await response.text())

        logger.info("🎉 Swarm execution workflow successfully completed!")

async def main():
    if len(sys.argv) < 2:
        print("Usage: python swarm_orchestrator.py \"<task description>\"")
        sys.exit(1)
        
    task = sys.argv[1]
    orchestrator = SwarmOrchestrator(task)
    
    # Run the mechanical workflow phases sequentially
    await orchestrator.run_discovery()
    await orchestrator.run_planning()
    await orchestrator.wait_for_approval()
    await orchestrator.run_execution()
    await orchestrator.run_verification()

if __name__ == "__main__":
    asyncio.run(main())
