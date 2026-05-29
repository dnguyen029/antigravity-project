# Technical Operations & Agent Management Portfolio

A production Python project built on the **Google Antigravity 2.0 SDK**, housing two distinct AI systems: a **live customer-facing receptionist** deployed to Google Cloud Run and a **governed multi-agent swarm** for structured engineering tasks.

---

## 🤖 System 1 — Multi-Agent BYOC Receptionist

A standalone, decoupled AI receptionist handling inbound customer contacts for **\[Customer Storefront Name\]** (an Adobe Commerce/Magento storefront). The system classifies caller intent in real time and routes to a specialized subagent — without ever disclosing it's an AI.

### What It Does

Incoming Call / Message

        │

        ▼

   Router Agent  ──── intent: Lead Capture ──▶ After Hours Receptionist ──▶ Google Sheets

        │

        ├─── intent: Order Tracking / WISMO ──▶ WISMO Receptionist ──▶ Zendesk Ticket Lookup

        │

        └─── intent: General FAQ ────────────▶ FAQ Receptionist ──▶ Grounded Answer

### Commitment to Quality & Security

- **Risk Mitigation via Isolation** — The client-facing service is fully decoupled from core engineering, ensuring zero operational cross-contamination.  
- **Confidentiality & Privacy** — Specialized logic is kept in secure, isolated containers to prevent sensitive data leakage.  
- **Enhanced Client Experience** — Strict communication guidelines are enforced to ensure professional, concise, and helpful interactions.  
- **Data Integrity Checks** — Comprehensive lead profiles are validated against strict formatting standards before processing.  
- **Mandatory Verification** — Quality assurance protocol requires formal confirmation of all contact details before any system update.

### Production Deployment

| Property | Value |
| :---- | :---- |
| Platform | Google Cloud Run |
| GCP Project | "GCP projectID" |
| Service Name | "GCP service name" |
| Region | "GCP region" |
| Auth | "Google Default Identity (OIDC)" |

### Webhook Endpoints

| Route | Purpose |
| :---- | :---- |
| `/webhook/write-to-sheets` | Lead capture → Google Sheets \+ Zendesk |
| `/webhook/wismo-lookup` | Order status lookup by PO number |
| `/webhook/faq-lookup` | Grounded FAQ answer from knowledge base |

---

## ⚙️ System 2 — Governed Quartet Swarm

A 5-agent engineering swarm with **enforcement-based governance** — not just rules, but programmatic gates that physically block execution until conditions are met. Designed for structured, auditable development tasks.

### Roles and Responsibilities

###

| Agent | Role | Decision-Making Authority  |
| :---- | :---- | :---- |
| **orchestrator** | Principal Architect | Task delegation and high-level architecture  |
| **builder** | Lead Developer | Core implementation and systems integration  |
| **auditor** | Compliance & Quality Control  | Reviewing all output against security standards  |
| **admin** | Infrastructure Management  | Optimizing system configuration and environment  |
| **librarian** | Documentation & Record Keeping  | **Sole Record Custodian** for all permanent project data  |

All other agents have read/query access to memory stores; write access is sovereign to the Librarian.

### The 4-Phase Workflow

Every task passes through four programmatic phases enforced by `swarm_orchestrator.py`:

1\. Discovery  →  2\. Planning  →  3\. Execution  →  4\. Verification

**Root Cause Gate** — A hardcoded checkpoint in `swarm_orchestrator.py` that blocks all file modifications unless `implementation_plan.md` contains a valid Root Cause Analysis documenting: (1) visible symptoms, (2) technical root cause, and (3) permanent resolution plan. Cannot be bypassed by any agent.

**Plan Approval Gate** — No writes to code or configuration files, and no terminal commands (beyond research), until the user explicitly approves the drafted plan.

### Governance Framework (Enforced Protocols)

###

| Rule | Policy Mandate  |
| :---- | :---- |
| Focused Scope Management  | Prevent scope creep by delivering exactly what is requested while documenting future needs.  |
| Diagnose Before Fix | Mandatory diagnosis phase before any action. Stops work to seek clarification if ambiguity exists.  |
| Validated Search Policy  | Requires use of high-authority knowledge sources over generic public data.  |
| Safety Boundaries | Compliance with budget constraints and safety protocols to protect system stability.  |
| Historical Context Review  | Review of past project context is required before drafting new plans to ensure continuity.  |
| Plan Approval Gate  | Prevents unauthorized implementation by requiring explicit stakeholder sign-off.  |
| Resource Optimization  | Advanced Infrastructure Cost Control: Strict focus on token efficiency, enforced via the internal Model Context Protocol (MCP) standard, to aggressively manage cloud budget and prevent wasteful spending.  |
| Objective Integrity  | Prioritizes sound engineering over following flawed instructions.  |
| Zero Inference Standard  | Decisions based on verified data only. Ambiguity triggers a stop-work-and-verify protocol.  |

### Compliance Audit — SUCCESSFUL (May 2026\)

###

| Policy Verified  | Status | Notes |
| :---- | :---- | :---- |
| Resilience Protocol  | ✅ PASSED | Systems continue to function safely even during partial network interruptions  |
| Data Sovereignty  | ✅ PASSED | Strict access controls prevent unauthorized team members from modifying permanent records  |
| Operational Isolation  | ✅ PASSED | Verified that project environments are isolated to prevent cross-account risk  |
| Secure Logic Encapsulation  | ✅ PASSED | Client interaction rules are strictly contained and cannot bleed into engineering space  |

*Audit session archived to Supabase: `swarm_knowledge_archive`, session `363ad4088badda3924cec1ecfe5f2a10`*

---

## 🔧 Systems Integration Layer

Three core information services are integrated to support organizational memory and research:

| Service | Role |
| :---- | :---- |
| **Supabase** | Secured corporate memory bank (managed exclusively by the Documentation Lead)  |
| **Supermemory** | Intelligent knowledge retrieval for cross-session project context  |
| **Exa** | High-authority research and data gathering tools  |

---

## 📁 Repository Structure

antigravity-project/

├── main.py                    \# Webhook server \+ interactive test entrypoint

├── swarm\_orchestrator.py      \# Programmatic 4-phase workflow \+ approval gates

├── verify\_mcp\_connections.py  \# MCP health verifier

├── instructions/

│   ├── receptionist.txt       \# After Hours receptionist prompt \+ lead-capture rules

│   └── swarm\_agents.txt       \# Persona rules: Architect, Auditor, Builder, SRE, Librarian

├── tools/

│   ├── sheets.py              \# Google Sheets lead logger

│   └── zendesk.py             \# Zendesk Dual-PUT synchronizer

├── .agent/                    \# Antigravity 2.0 agent profile directory

├── AGENTS.md                  \# Agent roster \+ governance rules

├── RECEPTIONIST\_SOP.md        \# Receptionist architecture, endpoints, data schema

├── FINDINGS.md                \# Compliance audit log \+ MCP cleanup record

├── DOMAIN\_MAP.md              \# Domain topology

├── RIPPLE\_MAP.md              \# Change impact mapping

├── guardrails.md              \# Safety constraints and cost bounds

└── GEMINI.md                  \# Agent identity \+ Antigravity 2.0 configuration

---

## 🚀 Project Operations

\# Initialize automated services

python main.py

\# Run interactive agent session (local testing)

python main.py \--interactive

\# Run a governed swarm task

python swarm\_orchestrator.py "your task description here"

**Environment**: Requires a configured Python virtual environment with Antigravity 2.0 SDK installed and valid MCP credentials in environment variables. See `GEMINI.md` for full setup.

---

## Tech Stack

`Python 3` · `Google Antigravity 2.0 SDK` · `Google Cloud Run` · `Supabase` · `Supermemory` · `Exa Search` · `Google Sheets API` · `Zendesk API` · `MCP (Model Context Protocol)`  
