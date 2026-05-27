---
id: SECURITY
name: Security
severity: High
category: Governance
version: 1.0.0
---

# SECURITY.MD - Security Guardrails

> **Goal**: Protect the system from common vulnerabilities and human errors.



## 🛡️ 2. CODING STANDARDS (Secure Coding Standards)

1. **SQL Injection**:
   - Always use Parameterized Queries (or ORMs like Prisma/TypeORM).
   - Prohibit direct string concatenation in SQL statements.
2. **XSS (Cross-Site Scripting)**:
   - Sanitize all user or API input data.
   - Use libraries like `dompurify` when rendering HTML.
3. **Authentication**:
   - Always hash passwords (Bcrypt/Argon2).
4. **MFA Token Rotation (Verified Three)**:
   - The `SSM_MFA_TOKEN` MUST be rotated every 30 days or after any high-risk mission (T2).
   - Rotation requires generating a new 32-character high-entropy string and updating the `.env` file across all host nodes.
   - Access to the `a2a-private-key` is automatically revoked if the token is stale or missing.

---

## 🚨 3. INCIDENT PROTOCOL (Incident Protocol)

When discovering a vulnerability or suspected secret exposure:

1. **STOP**: Stop all current tasks.
2. **REPORT**: Immediately notify the user with a RED ALERT.
3. **REMEDY**: Propose key rotation or patching plans.
