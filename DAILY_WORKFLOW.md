# 📋 Antigravity 2.0: Daily Swarm Workflow Cheat Sheet

Welcome to your clean Antigravity 2.0 workspace! This is a simple, no-code guide to help you interact with your agent team, tag specialists, and use commands in your daily workflow.

---

## 🗣️ Option 1: Direct Chat (No Tags)
If you type in the chat box without tagging anyone, you are chatting directly with the **Principal Agent**.

> **When to use**: 
> * General questions (*"why did my build fail?"*)
> * Lightweight tasks or fast edits (*"clean up my background tasks"* or *"check my CPU status"*)
> * Asking for explanations in plain English.

---

## 🏷️ Option 2: Tagging Specialists
For structured tasks, you can summon a specific agent by tagging them (e.g. typing `@builder`). The IDE will load their specific instructions and tools.

| Agent Tag | Role | When to Tag Them | Example Request |
| :--- | :--- | :--- | :--- |
| **`@orchestrator`** | **Principal Architect** | Design plans, evaluate task scope, check dependencies. *(Cannot write code)* | `@orchestrator we need to design an integration for a new CRM system.` |
| **`@builder`** | **Lead Developer** | Write python code, create APIs, fix bugs, run syntax checks. | `@builder add a new customer sentiment column to tools/sheets.py` |
| **`@auditor`** | **Security & QA Auditor** | Review plans for safety, scan code for leaked keys, verify syntax. | `@auditor check our recent code edits to make sure they are secure.` |
| **`@librarian`** | **Technical Writer** | Document changes in walkthroughs, sync logs to Supabase, search memories. | `@librarian synchronize our active findings to the database.` |
| **`@admin`** | **SRE (Site Reliability)** | Manage environment variables, check configurations (`mcp_config.json`). | `@admin make sure our database connection settings are correct.` |

---

## ⌨️ Option 3: Slash Commands
Type `/` in the chat input bar to trigger automated shortcuts.

* **`/goal` (Deep Focus Mode)**: Use this for long-running, complex goals (like building a feature overnight) where you want the agent to work thoroughly without stopping.
* **`/browser` (Web Search)**: Use this to search the internet or web pages using our clean, bloat-free search engine.
* **`/grill-me` (Alignment Interview)**: Use this when you aren't sure how to design something. The agent will ask you a few simple multiple-choice questions to build the perfect plan.

---

## 🚀 How to Run the Automated Swarm
If you want to run the mechanical, sequential multi-agent workflow for a task, open the **Terminal panel** at the bottom of the desktop app and run:

```bash
/home/dnguyen029/venv/bin/python swarm_orchestrator.py "your task description here"
```

> [!TIP]
> **The Ideal Workflow**:
> 1. Tell **`@orchestrator`** what you want to build.
> 2. Review the plan in the right panel and approve it.
> 3. Tag **`@builder`** to write the code.
> 4. Tag **`@auditor`** or **`@librarian`** to verify and sync the results.

---

## 🔌 Pre-Flight: Verify MCP Connections
Before starting a session, you can confirm all 5 tool servers are healthy:

```bash
/home/dnguyen029/venv/bin/python verify_mcp_connections.py
```

This generates a `system_status_report.md` in the project root showing the connection status of every server (Supermemory, Exa, Supabase, TOON MCP, Context MCP).

---

## ⚡ Lightweight Alternative: Native Orchestrator
For simpler tasks that don't need the full 4-phase swarm governance, use the SDK-native orchestrator:

```bash
/home/dnguyen029/venv/bin/python native_orchestrator.py
```

This runs directly on the Antigravity 2.0 async SDK without the enforcement gates — faster for quick jobs, development testing, or one-off agent runs.

