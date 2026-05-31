#!/usr/bin/env python3
import sys
import json
import os

def main():
    try:
        # Read the tool call details from stdin
        input_data = sys.stdin.read()
        if not input_data.strip():
            print(json.dumps({"decision": "allow"}))
            return

        payload = json.loads(input_data)
        tool_call = payload.get("toolCall", {})
        tool_name = tool_call.get("name")
        arguments = tool_call.get("args", {})
    except Exception as e:
        # Fail closed on parse errors
        print(json.dumps({
            "decision": "deny",
            "reason": f"Safety gate validation failed to parse input: {str(e)}"
        }))
        return

    # 1. Prohibited Directories (Access Protection)
    prohibited_folders = [".venv", ".git", "venv", "node_modules"]
    paths_to_check = []
    for arg_name in ["path", "AbsolutePath", "DirectoryPath", "TargetFile", "SearchPath", "file_path"]:
        if arg_name in arguments and isinstance(arguments[arg_name], str):
            paths_to_check.append(arguments[arg_name])

    for file_path in paths_to_check:
        normalized_path = file_path.replace("\\", "/")
        parts = normalized_path.split("/")
        if any(folder in parts for folder in prohibited_folders):
            print(json.dumps({
                "decision": "deny",
                "reason": f"Access to prohibited directory path '{file_path}' is blocked."
            }))
            return

    # 2. Destructive Commands & Shell Guardrails
    if tool_name in ["run_command", "execute_command"]:
        cmd = arguments.get("CommandLine", "").strip()
        cmd_lower = cmd.lower()
        
        # Dangerous file deletion checks
        if "rm " in cmd_lower or "rmdir" in cmd_lower:
            # Block any rm command unless restricted to temp/safe folders
            if not any(safe_p in cmd_lower for safe_p in ["/tmp/", "scratch/"]):
                print(json.dumps({
                    "decision": "deny",
                    "reason": f"Destructive command blocked: execution of '{cmd}' is prohibited."
                }))
                return
                
        # Git history protection
        if "git " in cmd_lower and ("reset --hard" in cmd_lower or "push" in cmd_lower and "--force" in cmd_lower):
            print(json.dumps({
                "decision": "deny",
                "reason": "Destructive Git operations (hard resets, force pushes) are blocked."
            }))
            return

    # 3. Quota Optimization Guards (Broad Searches)
    if tool_name in ["grep_search", "list_dir"]:
        path_arg = arguments.get("SearchPath") or arguments.get("DirectoryPath") or ""
        # Block scanning workspace root or home too broadly
        if path_arg in ["/", "/home", "/home/dnguyen029", "/home/dnguyen029/antigravity-project", "/home/dnguyen029/antigravity-project/"]:
            if tool_name == "grep_search":
                query_arg = arguments.get("Query", "")
                if query_arg in ["", "*", ".*"] or len(query_arg) < 2:
                    print(json.dumps({
                        "decision": "deny",
                        "reason": f"Broad grep search on workspace root is blocked to optimize token/quota usage."
                    }))
                    return
            elif tool_name == "list_dir" and path_arg in ["/", "/home", "/home/dnguyen029"]:
                print(json.dumps({
                    "decision": "deny",
                    "reason": "Listing system root directories is blocked to prevent token waste."
                }))
                return

    # 4. Plan Approval Gate / Root Cause Gate (Writing/modifying files)
    write_tools = ["write_file", "edit_file", "write_to_file", "replace_file_content", "multi_replace_file_content", "delete_file"]
    if tool_name in write_tools:
        target_file = arguments.get("TargetFile") or arguments.get("file_path") or arguments.get("path") or ""
        target_basename = os.path.basename(target_file)
        
        # Don't restrict writing to plan/task/walkthrough files themselves
        if target_basename not in ["implementation_plan.md", "task.md", "walkthrough.md"]:
            plan_file = "implementation_plan.md"
            # Look at project root for implementation_plan.md
            workspace_plan = os.path.join("/home/dnguyen029/antigravity-project", plan_file)
            if not os.path.exists(workspace_plan) and not os.path.exists(plan_file):
                print(json.dumps({
                    "decision": "deny",
                    "reason": "Plan Approval Gate: 'implementation_plan.md' must exist before modifying code files."
                }))
                return
                
            plan_to_read = workspace_plan if os.path.exists(workspace_plan) else plan_file
            try:
                with open(plan_to_read, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                has_rca = "root cause" in content or "rca" in content
                has_proposed = "proposed changes" in content or "proposed" in content or "plan" in content
                if not (has_rca or has_proposed):
                    print(json.dumps({
                        "decision": "deny",
                        "reason": "Plan Approval Gate: 'implementation_plan.md' must document Root Cause Analysis (RCA) or Proposed Changes."
                    }))
                    return
            except Exception as e:
                print(json.dumps({
                    "decision": "deny",
                    "reason": f"Plan Approval Gate: Failed to read implementation plan: {str(e)}"
                }))
                return

    # 5. Database Modification Checks
    if tool_name == "execute_sql":
        query = arguments.get("query", "").strip().upper()
        write_keywords = ["INSERT ", "UPDATE ", "DELETE ", "DROP ", "CREATE ", "ALTER ", "REPLACE ", "TRUNCATE "]
        if any(kw in query for kw in write_keywords):
            print(json.dumps({
                "decision": "deny",
                "reason": "Modifying SQL query blocked by default safety policies."
            }))
            return

    # Default: Allow the tool execution
    print(json.dumps({"decision": "allow"}))

if __name__ == "__main__":
    main()
