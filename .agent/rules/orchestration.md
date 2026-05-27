---
id: ORCHESTRATION
name: Orchestration
severity: Medium
category: Governance
version: 1.0.0
agent:
  id: "orchestrator"
  capabilities:
    - "/plan"
    - "/status"
    - "/research"
  governance:
    tool_lockout: true
    prohibited_mutations:
      - "src/**/*"
      - "scripts/**/*"
    delegation_target: "builder"
  routing:
    state_file: "config/mission.json"
    telemetry_stream: "src/telemetry/streamer.js"
---

# ORCHESTRATION.MD - Architect Directives

> **Goal**: Enforce state-sync discipline for the Architect.

---
*Authorized by Team Guidelines*
