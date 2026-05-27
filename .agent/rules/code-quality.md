---
id: CODE_QUALITY
name: Code Quality
severity: Medium
category: Governance
version: 1.0.0
---

# CODE-QUALITY.MD - Engineering Excellence

> **Goal**: Ensure source code always reaches "Production-Grade" quality from the very first line of code.



## ✅ 2. Best Practices (Recommended)

1. **Naming Convention**:
   - Variable/Function: `camelCase` (e.g., `userProfile`)
   - Class/Component: `PascalCase` (e.g., `UserProfile`)
   - Constant: `SCREAMING_SNAKE_CASE` (e.g., `MAX_RETRIES`)
   - File: `kebab-case` (e.g., `user-profile.ts`)

2. **Comments**:
   - Explain "WHY", not "WHAT".
   - Use JSDoc/DocString for public functions.

3. **Error Handling**:
   - Always use `try/catch` for async/await.
   - Do not swallow errors (silent fail). Always log or throw them.

---

## 🧪 3. Testing Requirements

1. **Unit Test**: Complex logic must be accompanied by Unit Tests.
2. **Coverage**: Aim for > 80% coverage for core modules.
