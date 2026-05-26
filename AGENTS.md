# AGENTS.md - Antigravity Agent Team (v2.0)

This document lists the active agent team roles in the Antigravity 2.0 SDK project workspace.

---

## 🏗️ Swarm Agent Team Roles

| Agent ID | Role | Profile File | Key Focus / Responsibilities | Primary Tool Authority |
| :--- | :--- | :--- | :--- | :--- |
| **orchestrator** | **Principal Architect** | [architect.txt](file:///home/dnguyen029/antigravity-project/instructions/architect.txt) | Technical strategy, planning, and task delegation | Filesystem, planning tools |
| **builder** | **Lead Developer** | [builder.txt](file:///home/dnguyen029/antigravity-project/instructions/builder.txt) | Python script implementation and API integration | Local code editing, python compiler |
| **auditor** | **Lead Security & QA Auditor** | [auditor.txt](file:///home/dnguyen029/antigravity-project/instructions/auditor.txt) | Security auditing and policy compliance reviews | Safety policies checks |
| **admin** | **Site Reliability Engineer (SRE)** | [sre.txt](file:///home/dnguyen029/antigravity-project/instructions/sre.txt) | Workspace hygiene and MCP configurations | Configuration management (`mcp_config.json`) |
| **librarian** | **Technical Writer & Archivist** | [librarian.txt](file:///home/dnguyen029/antigravity-project/instructions/librarian.txt) | Documentation, log hygiene, database syncs | **Exclusive** access to Supabase & Supermemory |

---

## 🤖 Standalone Receptionist
* **ID**: `receptionist`
* **Profile File**: [receptionist.txt](file:///home/dnguyen029/antigravity-project/instructions/receptionist.txt)
* **Goal**: Ariel Bath AI Receptionist. Decoupled from the swarm; handles lead capture via Google Sheets and Zendesk.

---

## 🏛️ Swarm Rules & Mandates
- **Process Gate Rule**: All agents MUST strictly adhere to the programmatic SDK phases (Discovery, Planning & Root Cause Gate, Execution, Verification) managed mechanically in [swarm_orchestrator.py](file:///home/dnguyen029/antigravity-project/swarm_orchestrator.py).
- **Rule 1 — Minimum Viable Change**: Implement only what was explicitly requested. Do not add features, abstractions, or improvements beyond the stated task. If you see an opportunity to improve something adjacent, flag it — don't build it.
- **Rule 2 — Diagnose Before You Fix**: Before applying any fix, state the root cause in plain English. If you cannot identify the root cause, stop and ask. Do not patch symptoms.
  * *Root Cause Gate*: A programmatic checkpoint hardcoded in `swarm_orchestrator.py` that physically blocks all file modifications unless `implementation_plan.md` contains a valid Root Cause Analysis (RCA) section documenting: (1) the visible symptoms, (2) the technical root cause, and (3) the permanent resolution plan. This gate cannot be bypassed by any agent.
