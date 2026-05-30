I have drafted the **Implementation Plan** and **Task Checklist** for the `"verify status report"` routine. Following the **Write Policy Mandate**, I completed these as **append-only edits** to keep the existing webhook configurations and SDK migration history intact.

The planning files have been successfully modified and are ready for review:
1. **Implementation Plan Block**: Appended to [implementation_plan.md](file:///home/dnguyen029/antigravity-project/implementation_plan.md#L48).
2. **Task Checklist Block**: Appended to [task.md](file:///home/dnguyen029/antigravity-project/task.md#L11).

---

### 🏛️ Plan & Architecture Overview

#### 🔍 Root Cause Analysis (RCA)
* **Symptom**: Difficulty diagnosing active tool capabilities and handshake integrity across multiple remote/local MCP services ([supabase](file:///home/dnguyen029/antigravity-project/mcp_config.json#L49), `supermemory`, `exa`, `toon-mcp`).
* **Root Cause**: Absence of a unified pre-flight auditing tool and runtime boundary validation inside the custom orchestrator.
* **Resolution**: Maintain and execute [verify_mcp_connections.py](file:///home/dnguyen029/antigravity-project/verify_mcp_connections.py) to sweep background zombie processes, conduct program stdio JSON-RPC handshakes, and save the verified status report to [system_status_report.md](file:///home/dnguyen029/antigravity-project/system_status_report.md). Enforce strict security validation limits in [get_policies_for_role](file:///home/dnguyen029/antigravity-project/native_orchestrator.py#L68) to protect directories and conserve tokens.

#### 🛡️ Sovereign Connection Safeguards
* **Rule 1 (Dynamic Header Validation)**: The verification suite automatically skips handshakes on the Supabase SSE node if required access headers are missing, completely preventing connection boot hangs.
* **Rule 2 (Sovereign Database Custody)**: Standard credentials remain isolated inside secure environment configurations rather than exposed generally.

---

### 📋 Appended Task Checklist (inside [task.md](file:///home/dnguyen029/antigravity-project/task.md#L11))

* **Execute programmatic handshakes and sweep system processes via [verify_mcp_connections.py](file:///home/dnguyen029/antigravity-project/verify_mcp_connections.py)**
  * Terminate background zombie processes mapping to PPID 1 matching server signatures.
  * Run pre-flight JSON-RPC handshakes on stdio servers (`supermemory`, `exa`, `toon-mcp`) and output active tool lists.
  * Skip checking Supabase SSE when credentials are empty to avoid initialization jams.
* **Implement and verify policy boundaries inside [get_policies_for_role](file:///home/dnguyen029/antigravity-project/native_orchestrator.py#L68)**
  * Restrict broad-search queries on list directory and search commands.
  * Ban file altering tools when no active implementation plan exists.
  * Confine orchestrator capability profiles exclusively to planning markdown structures.
* **Compile and output results to [system_status_report.md](file:///home/dnguyen029/antigravity-project/system_status_report.md)**
* **Run python compiler check**: `/home/dnguyen029/.venv/bin/python -m py_compile verify_mcp_connections.py native_orchestrator.py`
* **Execute full integration test CLI**: `python native_orchestrator.py "verify status report"`

---

### Turn Summary
1. **Analyzed** the operational context of `"verify status report"` and mapped it to the system status reporting framework.
2. **Discovered** the current structures inside [verify_mcp_connections.py](file:///home/dnguyen029/antigravity-project/verify_mcp_connections.py) and [native_orchestrator.py](file:///home/dnguyen029/antigravity-project/native_orchestrator.py).
3. **Appended** the new Plan section detailing the Root Cause Analysis, Proposed Changes, and Verification steps to [implementation_plan.md](file:///home/dnguyen029/antigravity-project/implementation_plan.md).
4. **Appended** the new Task Tracker checks to [task.md](file:///home/dnguyen029/antigravity-project/task.md).