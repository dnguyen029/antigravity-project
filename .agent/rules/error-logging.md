---
id: ERROR_LOGGING
name: Error Logging
severity: Medium
category: Governance
version: 1.0.0
---

# ERROR-LOGGING.MD - Automatic Error Tracking & Learning

> **Goal**: Record every error that occurs during development to learn and improve. Prevent recurring errors.



## 📝 2. ERROR LOGGING FORMAT

Each error MUST comply with the following structure in `ERRORS.md`:

```markdown
## [YYYY-MM-DD HH:MM] - Brief Error Title

- **Type**: [Syntax/Logic/Integration/Runtime/Agent/Process]
- **Severity**: [Low/Medium/High/Critical]
- **File**: `path/to/file.extension:line_number`
- **Agent**: [Executing Agent Name]
- **Root Cause**: Root Cause Description (1-2 sentences)
- **Error Message**:
```

[Error code or stack trace]

```
- **Fix Applied**: Specific action taken
- **Prevention**: How to avoid repeating this error in the future
- **Status**: [Fixed/Investigating/Deferred]



## 🔄 3. AUTOMATIC PROCESS

1. **Error Detection**: When an Agent encounters an error (test fail, build fail, runtime error).
2. **Classification**: Determine Type and Severity.
3. **Recording**: Append to the `ERRORS.md` file following the standard format.
4. **Notification**: Inform the user that the error has been logged and provide the file path.
5. **Resolution**: Fix the error and update the Status.



## ⚠️ 5. IMPORTANT NOTES

1. **Never delete old errors**: Errors are learning assets.
2. **Always update Status**: Mark as Fixed when resolved.
3. **Privacy**: Do not log sensitive information (API Keys, Passwords).
4. **Periodic Review**: Review errors at the end of the week to learn from experience.

---

## 🎓 6. LEARNING FROM ERRORS

Every error repeating 2 times or more MUST be turned into:

- **New Rule**: To prevent automatically.
- **Test case**: To detect early.
- **Checklist item**: In the pre-flight check.
