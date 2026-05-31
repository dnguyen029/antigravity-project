---
id: TESTING_STANDARD
name: Testing Standard
severity: Medium
category: Governance
version: 1.0.0
---

# TESTING-STANDARD.MD - Quality Assurance Protocol

> **Goal**: "Code without Tests is Dead Code". Ensure all features run correctly as designed before Production.



## 📝 2. Naming Conventions

- **File Name**: `*.test.ts` or `*.spec.ts`.
- **Structure**:

  ```typescript
  describe('AuthService', () => {
    // Module Name
    describe('login()', () => {
      // Function Name
      it('should return token when creds are valid', () => {
        // Expected behavior
        // ...
      });

      it('should throw 401 when password wrong', () => {
        // Edge case
        // ...
      });
    });
  });
  ```



## 📊 4. Coverage Requirements

- **Core Logic**: > 80% Statement Coverage.
- **Utils/Helpers**: > 90% Coverage.
- **UI Components**: Test behavior, don't test implementation details.

> **Golden Rule:** "Red - Green - Refactor". Write a failing test first, then write code to pass it, and finally optimize.
