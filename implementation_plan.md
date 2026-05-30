# Plan: Migrate Custom Swarm Orchestrator to Native Antigravity 2.0 SDK

This plan details the migration of the custom state machine (`swarm_orchestrator.py`) to the native Google Antigravity 2.0 SDK. It leverages lifecycle hooks, safety policies, dynamic subagents, and auto-discovered workspace skills.

## Root Cause Analysis (RCA)
* **Symptom**: Higher token consumption per agent turn, custom coordination code complexity, and manual tool policy check loops in `swarm_orchestrator.py`.
* **Root Cause**: The orchestrator is running a custom-written Python state machine to manage agent phases (Discovery, Planning, Execution, Verification) and tool authorization instead of using native Antigravity 2.0 SDK constructs.
* **Resolution**: Deprecate the custom orchestration state loop. Standardize the multi-agent execution flow using native `Agent` contexts, dynamic subagent structures, and system-level `policy` hooks. Package the existing Sheets and Zendesk tools into native `.agent/skills/` folders.

---

## User Review Required

> [!IMPORTANT]
> The custom `swarm_orchestrator.py` will be kept intact during the migration as a fallback. The new native SDK code will be implemented in a new entrypoint `native_orchestrator.py` or integrated into `main.py` to prevent breaking active environments until fully verified.

---

## Proposed Changes

### Core Orchestration
#### [NEW] [native_orchestrator.py](file:///home/dnguyen029/antigravity-project/native_orchestrator.py)
* Initialize `LocalAgentConfig` and instantiate native async `Agent` contexts.
* Implement native safety policy array (`hooks.policy.deny`, `hooks.policy.allow`, `hooks.policy.ask_user`) replacing the manual `verify_tool_policy` functions.
* Set up a clean `main` loop that delegates tasks to subagents cleanly.

### Skills & Modular Tools
#### [NEW] [SKILL.md (Zendesk)](file:///home/dnguyen029/antigravity-project/.agent/skills/zendesk/SKILL.md)
* Define the Zendesk skill configuration, importing the current zendesk tool logic.
#### [NEW] [SKILL.md (Sheets)](file:///home/dnguyen029/antigravity-project/.agent/skills/sheets/SKILL.md)
* Define the Google Sheets logging skill configuration.

### Deprecation & Cleanup
#### [MODIFY] [swarm_orchestrator.py](file:///home/dnguyen029/antigravity-project/swarm_orchestrator.py)
* Add a deprecation warning comment at the top of the file pointing to `native_orchestrator.py`.

---

## Verification Plan

### Automated Tests
* Run python compiler syntax check on `native_orchestrator.py`.
* Run test run execution via CLI: `python native_orchestrator.py "verify status report"`

### Manual Verification
* Inspect the terminal outputs to ensure that the native user approval prompts activate correctly when `ask_user` policies are triggered.
