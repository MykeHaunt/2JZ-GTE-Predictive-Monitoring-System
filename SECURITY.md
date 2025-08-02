# Security Policy for 2JZ‑GTE‑Predictive‑Monitoring‑System

This document outlines supported versions and reporting procedures for security vulnerabilities in the **2JZ‑GTE‑Predictive‑Monitoring‑System** repository.

---

## ✅ Supported Versions

| Version Line      | Status         | Release Range               | Notes                                     |
|-------------------|----------------|-----------------------------|-------------------------------------------|
| **v1.0.x**        | ✅ Supported   | May 2024 → Present          | Stable production releases                |
| **v1.1.x (beta)** | 🟡 Maintenance | From Jul 1 2025              | Feature preview; experimental and limited support |
| **< v1.0.0**      | ❌ End‑of‑life | Before May 2024              | No longer receives security patches       |

Please report any security issues only for versions listed in the _Supported_ table. Fixes will not be provided for end‑of‑life versions.

---

## 🛡️ Reporting a Vulnerability

If you discover a potential security vulnerability, **do not open a public GitHub issue or pull request**.

### Preferred Reporting Channels

1. **Email** us at: **`security[at]2jz‑predict.com`**  
   (Use PGP key ID `0xF1A2B3C4D5E6F789` to encrypt)  
   *or*

2. **GitHub Security Advisory Form**  
   Submit via **`Security → Report a vulnerability`** in this repository. [oai_citation:1‡GitHub Docs](https://docs.github.com/en/enterprise-cloud%40latest/copilot/tutorials/copilot-chat-cookbook/analyze-security/secure-your-repository?utm_source=chatgpt.com) [oai_citation:2‡GitHub Docs](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository?utm_source=chatgpt.com) [oai_citation:3‡GitHub Docs](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/security-hardening-for-github-actions?utm_source=chatgpt.com) [oai_citation:4‡GitHub Docs](https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository?utm_source=chatgpt.com) [oai_citation:5‡GitHub Docs](https://docs.github.com/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability?utm_source=chatgpt.com)

---

## 📥 What to Include

Please include as much of the following as possible to help with triage:

- Project version, environment, and tested operating system.
- A clear description of the vulnerability.
- Repro steps or sample code (preferably minimal).
- Logs, stack traces, or screenshots illustrating the issue.
- A brief assessment of severity (e.g., “remote code execution”, “data leakage”).

---

## ⏳ Response & Fix Timeline

| Stage              | Timeline                               |
|--------------------|----------------------------------------|
| **Acknowledgment** | Within **3 business days**             |
| **Triage & Prioritization** | Typically within **7 business days**      |
| **Fix Deployment** | Critical/P1: within **14 calendar days**; P2/P3: next minor release |
| **Public Disclosure** | Upon release of fix, or after **90 days** of no response from reporter [oai_citation:6‡GitHub Docs](https://docs.github.com/en/enterprise-cloud%40latest/copilot/tutorials/copilot-chat-cookbook/analyze-security/secure-your-repository?utm_source=chatgpt.com) |

We will credit you as the discoverer when a fix is published, unless requested otherwise.

---

## 🧭 Responsible Disclosure Guidelines

- Keep all vulnerability information **confidential** until a fix is available.
- Act in good faith and do not exploit the vulnerability further than needed for proof‑of‑concept.
- Allow reasonable remediation time before public disclosure; typically—up to **90 days** from acknowledgment.
- Avoid posting public notices or social‑media discussion until after the patch is released.

---

## 🧪 Scope

We consider a submission a **“security issue”** if any of the following are affected:

- Remote code execution, privilege escalation, or arbitrary file write/read.
- Injection flaws (SQL, OS command, template, etc.).
- Credential exposure or insecure credential handling.
- Critical cryptographic vulnerabilities (e.g. TLS downgrade).
- Broken or missing authorization checks.

**Excluded**: styling bugs, performance issues, non‑confidential logic errors (like incorrect math or physics), or feature requests that do not pose a security risk.

---

## 🧠 For Maintainers: Security Best Practices

- **Enable private vulnerability reporting** on the repo so researchers can submit issues securely. [oai_citation:7‡GitHub Docs](https://docs.github.com/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability?utm_source=chatgpt.com) [oai_citation:8‡GitHub Docs](https://docs.github.com/en/enterprise-cloud%40latest/copilot/tutorials/copilot-chat-cookbook/analyze-security/secure-your-repository?utm_source=chatgpt.com) [oai_citation:9‡GitHub Docs](https://docs.github.com/en/code-security/getting-started/auditing-security-alerts?utm_source=chatgpt.com)
- **Enable Dependabot alerts**, version updates, and CodeQL scanning to catch vulnerable dependencies early. [oai_citation:10‡GitHub Docs](https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository?utm_source=chatgpt.com)
- **Designate a CODEOWNERS file** for critical folders to enforce reviews on changes.
- **Secure GitHub Actions workflows**:  
  - Use `GITHUB_TOKEN` with least‑privilege access.  
  - Mask secrets and regularly revoke/rotate them.  
  - Pin third‑party actions and update them regularly via Dependabot. [oai_citation:11‡GitHub Docs](https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/security-hardening-for-github-actions?utm_source=chatgpt.com) [oai_citation:12‡GitHub Docs](https://docs.github.com/en/actions/reference/security/secure-use?utm_source=chatgpt.com)

---

## 📚 Additional Resources

- Example `SECURITY.md` formats from Electron and Keycloak. [oai_citation:13‡GitHub Docs](https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository?utm_source=chatgpt.com)  
- GitHub Docs on coordinated disclosure and repository advisories. [oai_citation:14‡GitHub Docs](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/about-coordinated-disclosure-of-security-vulnerabilities?utm_source=chatgpt.com)

---

*This policy is in accordance with GitHub’s recommended security guidelines and responsible‑disclosure standards.*  
