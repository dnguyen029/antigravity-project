# 🍎 OWASP Top 10 - 2025 Edition (Antigravity Armor)

List of the most critical security vulnerabilities and how to prevent them.

1. **Broken Access Control**: Users accessing data that doesn't belong to them.
   - _Fix_: Check ID ownership at the Database level.
2. **Cryptographic Failures**: Exposure of sensitive data due to weak encryption.
   - _Fix_: Use AES-256 for data at rest and TLS 1.3 for data in transit.
3. **Injection (XSS, SQLi)**: Malicious code injected into commands.
   - _Fix_: Always use Parameterized Queries for SQL and Sanitize Input for FE.
4. **Insecure Design**: Architectural design flaws.
   - _Fix_: Perform Threat Modeling before coding.
5. **Security Misconfiguration**: Incorrect settings (default passwords, open ports).
   - _Fix_: Automate infrastructure configuration scanning.

---

### 🧪 Pentest Check:

Agents using this Skill MUST check these 5 points for every PR (Pull Request).
