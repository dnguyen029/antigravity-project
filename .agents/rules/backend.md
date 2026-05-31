---
id: BACKEND
name: Backend
severity: Medium
category: Governance
version: 1.0.0
---

# BACKEND.MD - Systems & Logic Standards

> **Goal**: A single set of rules managing all Logic, Data, and Infrastructure. High performance - No overlaps.



## 🗄️ 2. DATABASE MASTERY (DBA Mode)

1. **Schema Design**:
   - Adhere to 3NF (Third Normal Form).
   - `snake_case` for table/column names.
   - Always include `created_at`, `updated_at`.
2. **Performance**:
   - **Index**: Mandatory Index for foreign keys (FK) and search columns.
   - **Migration**: Never modify columns directly in Production. Create a new migration file.



## 🛡️ 4. ERROR HANDLING

1. **Structured Logging**: Logs must be parsable (JSON). DO NOT use `print`/`console.log`.
2. **Graceful Failure**: If DB dies, API returns 503; do not hang the request.
