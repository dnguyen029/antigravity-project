# 🛡️ Swarm Safety Guardrails

This document establishes the mandatory safety constraints and execution boundaries for all agents operating in this workspace.

---

## 🕒 1. Runaway Loop & Cost Prevention (Cost Guardrail)

* **Rule**: If any tool, script, or command fails **3 times in a row**, you MUST immediately stop, halt all loops, and escalate to the user.
* **Instruction**: Do not attempt to retry or troubleshoot endlessly. Explain the error in simple terms and wait for instructions.

## 🗑️ 2. Destructive Actions Blockade (Data Loss Guardrail)

* **Rule**: You are strictly prohibited from executing commands that perform destructive file or database operations without explicit user confirmation.
* **Blocked Actions**:
  * Deleting code files or project folders (`rm -rf` outside temp directories).
  * Hard resetting git history (`git reset --hard` or force-pushes).
  * Dropping database tables or deleting rows in production tables without verification.

## 🔑 3. Credentials & Secrets Isolation (Security Guardrail)

* **Rule**: Never hardcode API keys, passwords, bearer tokens, or database access strings in any file, script, or commit.
* **Instruction**: Load all configurations dynamically from environment variables (sourcing from `.env`). Never add `.env` or other key files to Git staging.

## 📦 4. Dependency & Bloat Control (Environment Hygiene)

* **Rule**: Do not install new third-party packages, libraries, or global system dependencies (e.g. `pip install`, `npm install`) without first asking the user for authorization.
* **Instruction**: Leverage existing utilities and native modules to keep the workspace clean and lightweight.

## 💡 5. Visionary Intent & Simplification

* **Rule**: Focus on the user's ultimate goal rather than the literal steps they suggest.
* **Instruction**: If the user proposes a 3-step technical path (e.g., do X, Y, Z), but a simpler, more standard, or more reliable 2-step solution exists, you MUST proactively inform the user and recommend the simpler alternative.

## 🏛️ 6. Mandatory Database Search & Plan Approval Gate

* **Rule**: All agents must check Supermemory and Supabase before planning or writing any code, and must halt execution to wait for plan approval.
* **Instruction**:
  * **Memory Audit**: You must perform read/query searches against Supermemory and Supabase database memories to locate lessons learned, design standards, and context files before drafting plans or writing code.
  * **Approval Gate**: You must write an `implementation_plan.md` plan and halt execution to await user approval. No direct code edits or command execution is permitted until the user explicitly approves the plan.

## 🏛️ 7. Quota Optimization & Batching

* **Rule**: All agents must minimize token usage and quota consumption by avoiding redundant scans and batching tool operations.
* **Instruction**:
  * **Broad Scans Blocked**: You are prohibited from running recursive workspace directory listings (`list_dir`) or broad wildcard searches (`grep_search` with no specific targets) over the workspace root.
  * **Targeted Operations**: Focus all tool executions only on the files explicitly specified in the approved implementation plan.
  * **Batching Work**: Combine edits into a single tool invocation (e.g. using `multi_replace_file_content`) and aggregate queries to minimize overall API turns.

## 🏛️ 8. Zero Sycophancy & Zero Inference

* **Rule**: All agents must maintain complete objectivity and operate strictly on verified parameters and facts without guessing.
* **Instruction**:
  * **Objective Truth**: Correct the user immediately and neutrally if they propose unsound technical designs, illogical paths, or violate instructions. Do not write sycophantic approvals.
  * **Explicit Inputs Only**: Stop and ask for clarification if parameters, files, or requirements are ambiguous or unspecified. Do not infer or guess intent.
