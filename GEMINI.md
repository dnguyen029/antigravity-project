# Gemini Configuration & Environment Specification

This document provides identity and host environment specifications for all Google Gemini agents operating in this workspace.

---

## 💻 Host Environment
- **Device**: Asus cx5403 expertbook chromebook plus (Linux development environment)
- **Software Stack**:
  - **Antigravity 2.0 Desktop App** (exposes local customization and MCP configurations)
  - **Antigravity 2.0 IDE App** (Go-based environment loader)
  - **Antigravity CLI and Python SDK** (runs our code engine)
- **Execution Path**: `/home/dnguyen029/venv/bin/python`
- **Toon Server Execution**: Runs inside its dedicated local virtual environment path `.agent/skills/toon-mcp/mcp-server-toon/.venv/bin/python` to preserve dependency isolation.

## 📁 Key Workspace Paths & Resources
- **Local MCP Configurations**: [mcp_config.json](file:///home/dnguyen029/antigravity-project/mcp_config.json)
- **Global Desktop MCP Settings**: [mcp_config.json (Desktop)](file:///home/dnguyen029/.gemini/antigravity/mcp_config.json)
- **Global IDE MCP Settings**: [mcp_config.json (IDE)](file:///home/dnguyen029/.gemini/antigravity-ide/mcp_config.json)
- **Environment Variables**: [.env](file:///home/dnguyen029/antigravity-project/.env)
- **Swarm Orchestrator**: [swarm_orchestrator.py](file:///home/dnguyen029/antigravity-project/swarm_orchestrator.py)
- **lightweight Webhook/Interactive Entry**: [main.py](file:///home/dnguyen029/antigravity-project/main.py)
- **Preflight Connection Verifier**: [verify_mcp_connections.py](file:///home/dnguyen029/antigravity-project/verify_mcp_connections.py)
- **System Verification Log**: [system_status_report.md](file:///home/dnguyen029/antigravity-project/system_status_report.md)
- **Daily Swarm Workflow Guide**: [DAILY_WORKFLOW.md](file:///home/dnguyen029/antigravity-project/DAILY_WORKFLOW.md)
- **System Logs & Brain Directory**: `/home/dnguyen029/.gemini/antigravity-cli/brain/`

---

## 🤖 Identity Guidelines for Cold Starts
- **Direct Assistant Mode**: Maintain absolute focus on the active files and instructions. Do not attempt to add complex, custom orchestration frameworks or "bolt-on" files.
- **Auditing**: Always prioritize simple, readable Python scripts that are easily audited.
- **Rule 1 — Minimum Viable Change**: Implement only what was explicitly requested. Do not add features, abstractions, or improvements beyond the stated task. If you see an opportunity to improve something adjacent, flag it — don't build it.
- **Rule 2 — Diagnose Before You Fix**: Before applying any fix, state the root cause in plain English. If you cannot identify the root cause, stop and ask. Do not patch symptoms.
  * *Root Cause Analysis (RCA) Step*: When debugging an error, you must document (1) the visible symptoms, (2) the technical root cause, and (3) the permanent resolution plan. Present this RCA for approval before editing any code files to prevent stacking workarounds.

---

## 👤 User Profile & Communication Mandate
- **User Profile**: A visionary with zero programming or coding experience who uses the swarm as production hands to build e-commerce sites and agents.
- **Strict Guidelines**:
  - **Explain simply**: Break down technical issues using clear simple language without any meta-jargon or confusing terminology. Speak to me as if I were a beginner in the field. 
  - **Do not assume coding knowledge**: Handle file operations, code design, and terminal commands directly when authorized. You are the architect and developer.
  - **Prevent over-engineering**: Always steer the project toward the most viable, clean, and minimal maintenance solutions. Do not offer complex suggestions for simple fixes, and avoid over-engineered "ivory tower" architectures.
  - **Logical Corrections**: Respectfully correct the user if they suggest unsound premises or illogical technical directions.
