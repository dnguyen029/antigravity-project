# **Technical Operations & Agent Management Portfolio**

A production Python project built on the **Google Antigravity 2.0 SDK** and the **Google Agents SDK (ADK)**, housing two distinct AI systems: a **live customer-facing receptionist** deployed to Google Cloud Run and a **governed multi-agent swarm** for structured engineering tasks.

## **🤖 System 1 — Multi-Agent BYOC Receptionist**

A standalone, decoupled AI receptionist handling inbound customer contacts for a headless digital storefront ecosystem. The system classifies caller intent in real time and routes to a specialized subagent via the **Agents CLI** and **A2A (Agent-to-Agent)** framework—without ever disclosing it's an AI.

### **What It Does**

Incoming Call / Message (Next.js Frontend)

│

▼

Router Agent ──── intent: Lead Capture ──▶ After Hours Receptionist ──▶ Google Sheets

│

├─── intent: Order Tracking / WISMO ──▶ WISMO Receptionist ──▶ Medusa / Shopify API / Zendesk Ticket Lookup

│

└─── intent: General FAQ ────────────▶ FAQ Receptionist ──▶ Grounded Answer (Contentful / Sanity.io CMS)

### **Commitment to Quality & Security**

* **Headless Commerce Orchestration** — Decoupled frontend built with **Next.js** interacting seamlessly with **Medusa** and **Shopify** API-first backends via custom webhook event structures.  
* **Contentful & Sanity.io Sync** — Dynamic schema configuration pulling directly from headless CMS layers to ground agent FAQ workflows.  
– Integrated UI/UX CMS Studio to edit content directly from the GUI 
* **Risk Mitigation via Isolation** — The client-facing service is fully decoupled from core engineering, ensuring zero operational cross-contamination.  
* **Confidentiality & Privacy** — Specialized logic is kept in secure, isolated containers to prevent sensitive data leakage.  
* **Data Integrity Checks** — Comprehensive lead profiles are validated against strict formatting standards before processing.  
* **Mandatory Verification** — Quality assurance protocol requires formal confirmation of all contact details before any system update.

### **Production Deployment**

| Property | Value |
| :---- | :---- |
| Platform | Google Cloud Run |
| Service Name | receptionist-prod |
| Region | us-west1 |
| Auth | Google Default Identity (OIDC) |
| Environment | Vercel & Railway |

### **Webhook Endpoints**

| Route | Purpose |
| :---- | :---- |
| /webhook/write-to-sheets | Lead capture → Google Sheets \+ Zendesk |
| /webhook/wismo-lookup | Order status lookup by PO number via backend APIs |
| /webhook/faq-lookup | Grounded FAQ answer from headless CMS knowledge base |

## **⚙️ System 2 — Governed Quartet Swarm**

A 5-agent engineering swarm featuring strict, programmatic enforcement gates via swarm\_orchestrator.py. Designed for structured, auditable development tasks with **enforcement-based governance**.

### **Roles and Responsibilities**

| Agent | Role | Decision-Making Authority |
| :---- | :---- | :---- |
| **orchestrator** | Principal Architect | Task delegation and high-level architecture |
| **builder** | Lead Developer | Core implementation and systems integration |
| **auditor** | Compliance & Quality Control | Reviewing all output against security standards |
| **admin** | Infrastructure Management | Optimizing system configuration and environment |
| **librarian** | Documentation & Record Keeping | **Sole Record Custodian** for all permanent project data |

All other agents have read/query access to memory stores; write access is sovereign to the Librarian.

### **The 4-Phase Workflow**

Every task passes through four programmatic phases enforced by swarm\_orchestrator.py:

1\. Discovery → 2\. Planning & Root Cause Gate → 3\. Execution → 4\. Verification

**Root Cause Gate** — A hardcoded checkpoint in swarm\_orchestrator.py that blocks all file modifications unless implementation\_plan.md contains a valid Root Cause Analysis documenting: (1) visible symptoms, (2) technical root cause, and (3) permanent resolution plan. Cannot be bypassed by any agent.

**Plan Approval Gate** — No writes to code or configuration files, and no terminal commands (beyond research), until the user explicitly approves the drafted plan.

### **Governance Framework (Enforced Protocols)**

| Rule | Policy Mandate |
| :---- | :---- |
| Focused Scope Management | Prevent scope creep by delivering exactly what is requested while documenting future needs. |
| Diagnose Before Fix | Mandatory diagnosis phase before any action. Stops work to seek clarification if ambiguity exists. |
| Validated Search Policy | Requires use of high-authority knowledge sources over generic public data. |
| Safety Boundaries | Compliance with budget constraints and safety protocols to protect system stability. |
| Historical Context Review | Review of past project context is required before drafting new plans to ensure continuity. |
| Plan Approval Gate | Prevents unauthorized implementation by requiring explicit stakeholder sign-off. |
| Resource Optimization | **TOON MCP Server Execution:** Strict token efficiency enforced via Token-Oriented Object Notation servers, compressing verbose JSON payloads to reduce LLM overhead by 40–60%. |
| Objective Integrity | Prioritizes sound engineering over following flawed instructions. |
| Zero Inference Standard | Decisions based on verified data only. Ambiguity triggers a stop-work-and-verify protocol. |

### **Compliance Audit — SUCCESSFUL (May 2026\)**

| Policy Verified | Status | Notes |
| :---- | :---- | :---- |
| Resilience Protocol | ✅ PASSED | Systems continue to function safely even during partial network interruptions |
| Data Sovereignty | ✅ PASSED | Strict access controls prevent unauthorized team members from modifying permanent records |
| Operational Isolation | ✅ PASSED | Verified that project environments are isolated to prevent cross-account risk |
| Secure Logic Encapsulation | ✅ PASSED | Client interaction rules are strictly contained and cannot bleed into engineering space |

*Audit session archived to Supabase: swarm\_knowledge\_archive, session 363ad4088badda3924cec1ecfe5f2a10*

## **🔧 Systems Integration Layer**

Four core information services are integrated to support organizational memory, token compression, and research:

| Service | Role |
| :---- | :---- |
| **TOON MCP Server** | Custom Model Context Protocol server executing row-based token payload compression. |
| **Supabase** | Secured corporate memory bank (managed exclusively by the Documentation Lead). |
| **Supermemory** | Intelligent knowledge retrieval for cross-session project context. |
| **Exa** | High-authority research and data gathering tools. |

## **📁 Repository Structure**

Plaintext  
antigravity-project/  
├── main.py                      \# Webhook server \+ interactive test entrypoint  
├── swarm\_orchestrator.py        \# Programmatic 4-phase workflow \+ approval gates  
├── native\_orchestrator.py       \# SDK-native orchestrator (Antigravity 2.0 async)  
├── verify\_mcp\_connections.py    \# MCP health verifier \+ system status report generator  
├── tools/  
│   ├── sheets.py                \# Google Sheets lead logger  
│   ├── zendesk.py               \# Zendesk Dual-PUT synchronizer  
│   └── context\_mcp\_server.py   \# Local context MCP server  
├── .agents/                     \# Antigravity 2.0 agent directory  
│   ├── agents/                  \# Subagent instructions and persona configurations  
│   │   ├── receptionist.txt  
│   │   ├── architect.txt  
│   │   ├── builder.txt  
│   │   ├── auditor.txt  
│   │   ├── sre.txt  
│   │   └── librarian.txt  
│   ├── rules/                   \# Autonomic rules (AGENTS.md, GEMINI.md, etc.)  
│   ├── skills/                  \# Reusable agent skills  
│   └── hooks.json               \# Pre/post tool execution hook configuration  
├── AGENTS.md                    \# Agent roster \+ governance rules  
├── RECEPTIONIST\_SOP.md          \# Receptionist architecture, endpoints, data schema  
├── FINDINGS.md                  \# Compliance audit log \+ MCP cleanup record  
├── DOMAIN\_MAP.md                \# Domain topology  
├── RIPPLE\_MAP.md                \# Change impact mapping  
├── guardrails.md                \# Safety constraints and cost bounds  
└── GEMINI.md                    \# Agent identity \+ Antigravity 2.0 configuration

## **🚀 Project Operations**

Bash  
\# Run local environment configuration tracing via Antigravity IDE  
\# Initialize automated services  
python main.py

\# Run interactive agent session (local testing via Agents CLI)  
python main.py \--interactive

\# Run a governed swarm task  
python swarm\_orchestrator.py "your task description here"

\# Verify all 5 MCP server connections are healthy  
python verify\_mcp\_connections.py

**Environment**: Requires a configured Python virtual environment with Antigravity 2.0 SDK and Google Agents SDK installed, valid MCP credentials in environment variables, and configured webhooks pointing to Next.js/Vercel pipelines. See GEMINI.md for full setup.

## **Tech Stack**

Python 3 · JavaScript/TypeScript · Google Antigravity 2.0 SDK · Google Agents SDK (ADK) · Agents CLI · Google Antigravity IDE · Google Cloud Run · Next.js · Medusa · Shopify Backend · Contentful CMS · Sanity.io · Supabase · Supermemory · Exa Search · Google Sheets API · Zendesk API · MCP (Model Context Protocol) · TOON MCP Server

