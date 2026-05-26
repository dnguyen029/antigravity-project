# Ariel Bath - Antigravity 2.0 Receptionist & Swarm

This is a clean, decoupled, and 100% compliant Antigravity 2.0 SDK Python project. It houses the Ariel Bath AI Receptionist and instructions for the Quartet Swarm.

---

## 🏛️ Strict Workspace Mandates
* **No Legacy Bloat**: This project is completely free of Node.js Express server wrappers, Redis database caching, or custom OIDC socket loops.
* **No Bolt-ons or Patch Jobs**: All new features or integrations (e.g. RingCentral telephony connection) must be designed directly into the core Python architecture, never added as external wrappers.
* **Python Environment**: Reuses the global user virtual environment at `/home/dnguyen029/venv` directly (avoiding local venv setup).

---

## 📁 Directory Map

* [main.py](file:///home/dnguyen029/antigravity-project/main.py): Entry point for running the webhook server or interactive test mode.
* [swarm_orchestrator.py](file:///home/dnguyen029/antigravity-project/swarm_orchestrator.py): Orchestration script that mechanically enforces the 4-phase swarm workflow and approval gates.
* [instructions/](file:///home/dnguyen029/antigravity-project/instructions/): Prompt directives for agents.
  - [receptionist.txt](file:///home/dnguyen029/antigravity-project/instructions/receptionist.txt): Rules and greeting workflows for the receptionist.
  - [swarm_agents.txt](file:///home/dnguyen029/antigravity-project/instructions/swarm_agents.txt): Persona rules for SRE, Architect, Auditor, Developer, and Technical Writer.
* [tools/](file:///home/dnguyen029/antigravity-project/tools/):
  - [sheets.py](file:///home/dnguyen029/antigravity-project/tools/sheets.py): Google Sheets database connector.
  - [zendesk.py](file:///home/dnguyen029/antigravity-project/tools/zendesk.py): Zendesk Dual-PUT synchronizer.
* [mcp_config.json](file:///home/dnguyen029/antigravity-project/mcp_config.json): Configuration file mapping Supabase, Exa, and Supermemory connections.

---

## 🚀 Commands

### Run Webhook Server (Default)
```bash
/home/dnguyen029/venv/bin/python main.py
```

### Run Interactive Agent (Local Trial)
```bash
/home/dnguyen029/venv/bin/python main.py --interactive
```

### Run Swarm Task (Programmatic 4-Phase Workflow)
```bash
/home/dnguyen029/venv/bin/python swarm_orchestrator.py "your task description here"
```
