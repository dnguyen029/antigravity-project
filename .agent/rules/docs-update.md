---
id: DOCS_UPDATE
name: Docs Update
severity: Medium
category: Governance
version: 1.0.0
---

# DOCS-UPDATE.MD - Documentation Sync Protocol

> **Goal**: Ensure documentation is always synchronized with actual code. Avoid outdated docs.



## 🔄 2. AUTOMATED PROCESS

1. **Change Detection**: After creating a new file in `.agent/`.
2. **Run Script**: `node scripts/lifecycle/update-docs.js`.
3. **Review Output**: The script will display current metrics.
4. **Manual Update**: Based on the checklist above.
5. **Commit Docs**: Create a separate commit for documentation.



## 🧹 4. CONSOLIDATION RULE

To prevent documentation bloat and fragmentation:

- **Avoid Single-Sentence Files**: Do not create a new `.md` file for a single rule or sub-skill. Consolidate into existing files.
- **Mission Archival**: All plans and walkthroughs MUST be moved to `mission/archive/` upon task completion.
- **Log Management**: Detailed tool logs or task IDs MUST be offloaded to telemetry files rather than being appended to progress files.

## ⚠️ 5. IMPORTANT NOTES

1. **English Only**: All documentation MUST be in English. Secondary language mirrors (e.g., Vietnamese) are strictly prohibited.
2. **Consistency**: Keep counts consistent; accurately count the number of files.
3. **Conciseness**: Write concise descriptions (1 line per skill/workflow).
4. **Separate Commits**: Isolate documentation updates in their own commits for easier review.

---

## 🎯 5. OBJECTIVES

- Documentation accurately reflects 100% of existing features.
- New users can understand the system solely from the README.
- No "hidden features" that are undocumented.
