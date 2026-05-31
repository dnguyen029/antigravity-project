# TEAM_GUIDELINES.md - Core Project Guidelines

> **Goal**: Define the foundational guidelines for the agent team.

## 🎯 Core Status
- **Project Status**: VERIFIED

## 🎯 1. Accuracy-First Rule
- **Protocol**: Accuracy is more important than speed. If any step has any ambiguity, agents MUST stop and request human clarification.
- **Verification**: No task is completed until the Security Auditor verifies code quality, security, and rule compliance.
- **Rule**: Agents must follow procedures strictly. If in doubt, STOP.

## 🏗️ 2. Stability and Quality Rule
- **Proven Solutions**: Prioritize well-understood, standard code structures over complex optimizations or new patterns that lack real-world presence.
- **Stability First**: If a design introduces excessive complexity that risks runtime stability, do not use it.
- **Verification**: Every code change must be verified via syntax checks and tests before completion.

## 🧩 3. Root-Cause Fix Rule
- **Root Cause First**: Agents MUST prioritize identifying and resolving the root cause of an issue.
- **No Temporary Patches**: Creating temporary patches or "shims" to mask an error is prohibited. A fix must address the root cause, not just the symptoms.
- **User Approval**: If a root-cause fix is complex or requires breaking architectural changes, the agent MUST halt execution, present the implementation plan to the user, and obtain approval before proceeding.

## 🎯 4. Proactive Guidance Rule
- **Non-Technical User**: The user is a non-technical director. Agents MUST NOT blindly execute user requests that could lead to over-engineering, security flaws, or instability. Proactively explain trade-offs and guide the user toward simple, stable solutions.

## 🎯 5. User Approval Rule
- **Explicit Instruction Only**: Under no circumstances should any agent perform any task, package installation, configuration change, or code update that was not explicitly requested or approved by the user.

## ⚖️ 6. Operational Invariants
1. **Role Separation**: No agent (including the Architect) shall perform modifications outside their role. Code edits must be delegated to the Developer.
2. **Log Tracking**: Every change must be documented and synchronized to the database.
3. **Dependency Audit**: All architectural changes must pass the dependency check script.

---
*Authorized by SRE | [VERIFIED]*
