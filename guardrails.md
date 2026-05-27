# 🛡️ Swarm Safety Guardrails

This document establishes the mandatory safety constraints and execution boundaries for all agents operating in this workspace.

---

## 🕒 1. Runaway Loop & Cost Prevention (Cost Guardrail)
* **Rule**: If any tool, script, or command fails **3 times in a row**, you MUST immediately stop, halt all loops, and escalate to the user.
* **Instruction**: Do not attempt to retry or troubleshoot endlessly. Explain the error in simple terms and wait for instructions.

## 🗑️ 2. Destructive Actions Blockade (Data Loss Guardrail)
* **Rule**: You are strictly prohibited from executing commands that perform destructive file or database operations without explicit user confirmation.
* **Blocked Actions**:
  - Deleting code files or project folders (`rm -rf` outside temp directories).
  - Hard resetting git history (`git reset --hard` or force-pushes).
  - Dropping database tables or deleting rows in production tables without verification.

## 🔑 3. Credentials & Secrets Isolation (Security Guardrail)
* **Rule**: Never hardcode API keys, passwords, bearer tokens, or database access strings in any file, script, or commit.
* **Instruction**: Load all configurations dynamically from environment variables (sourcing from `.env`). Never add `.env` or other key files to Git staging.

## 📦 4. Dependency & Bloat Control (Environment Hygiene)
* **Rule**: Do not install new third-party packages, libraries, or global system dependencies (e.g. `pip install`, `npm install`) without first asking the user for authorization.
* **Instruction**: Leverage existing utilities and native modules to keep the workspace clean and lightweight.

## 💡 5. Visionary Intent & Simplification
* **Rule**: Focus on the user's ultimate goal rather than the literal steps they suggest. 
* **Instruction**: If the user proposes a 3-step technical path (e.g., do X, Y, Z), but a simpler, more standard, or more reliable 2-step solution exists, you MUST proactively inform the user and recommend the simpler alternative.
