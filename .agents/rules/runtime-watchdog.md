---
id: RUNTIME_WATCHDOG
name: Runtime Watchdog
severity: Medium
category: Governance
version: 1.0.0
---

# RUNTIME-WATCHDOG.MD - Hang Detection & Execution Safety

> **Goal**: Prevent agents from hanging, falling into infinite loops, or responding too slowly, which wastes resources and disrupts the user experience.



## ⏱️ 2. EXECUTION TIMEOUTS

1. **Step Timeout**:
   - An execution step (a single tool call) should not exceed **60 seconds** (except for specific build/deploy commands).
   - If a child process is detected running for too long (> 5 minutes) without new output, the Agent MUST actively intervene (e.g., `taskkill` or sending a stop signal).

2. **Stuck UI Detection**:
   - When interacting with CLI prompts (like `prompts`, `inquirer`), the Agent MUST prioritize automatic flags (`--force`, `--skip-prompts`).
   - If interaction is mandatory and the UI does not change after 2 keystroke attempts, it MUST be considered hung and the process stopped.



## 📊 4. QUALITY CONTROL & MONITORING

- **Self-Monitoring**: The Agent tracks the number of execution steps for a Task. If it exceeds 20 steps without a positive result, it MUST stop to re-plan.
- **Log Error**: All hang incidents MUST be recorded in `/home/dnguyen029/.gemini/antigravity/mission/errors.md` according to the standard format for learning purposes.

---

> 🔴 **"An unresponsive agent is a broken agent."** - Always prioritize Responsiveness above all.
