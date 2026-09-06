# Application Threat Model & Data Flow Diagram (DFD)

## Target Architecture & System Boundary

This document outlines the threat model for the Python/Flask web service running within the automated DevSecOps pipeline.

```
[ External User / Attacker ]
│
│ (HTTP GET /search?q=)
▼
┌──────────────────────────────────────┐
│       Flask Application Server       │
│  - Port: 5000                        │
│  - Endpoint: /search                 │
└──────────────────┬───────────────────┘
│
│ (Unsanitized Render Input)
▼
┌──────────────────────────────────────┐
│     DOM / Client Web Browser         │
│  - Target: Reflected XSS             │
└──────────────────────────────────────┘
```
---

## STRIDE Threat Modeling Matrix

| Threat Category | Identified Vulnerability | Severity | Mitigation Strategy | Pipeline Detection Tool |
| :--- | :--- | :--- | :--- | :--- |
| **Spoofing** | Unauthenticated `/search` endpoint accessible without session verification. | Low | Implement OAuth 2.0 / JWT session authentication middleware. | OWASP ZAP (DAST) |
| **Tampering** | Parameterized inputs directly embedded into HTML responses via `render_template_string`. | High | Enforce Jinja2 auto-escaping or sanitize user inputs using `bleach`. | Semgrep (SAST) |
| **Repudiation** | Lack of structured security audit logging for incoming request payloads. | Medium | Implement standard JSON request/response logging to stdout/syslog. | Code Review |
| **Information Disclosure** | Verbose Flask server response headers exposed during endpoint scanning. | Low | Configure production WSGI server (Gunicorn) with customized header masking. | OWASP ZAP (DAST) |
| **Elevation of Privilege** | Reflected Cross-Site Scripting (XSS) allowing client-side script execution. | High | Enforce Content Security Policy (CSP) headers and input encoding. | Semgrep & ZAP |

---

## Automated Security Pipeline Controls

1. **Static Application Security Testing (SAST)**: Semgrep scans source code on pull requests to identify dangerous sink patterns (e.g., `render_template_string`, raw SQL queries).
2. **Dynamic Application Security Testing (DAST)**: OWASP ZAP executes baseline vulnerability tests against running container instances on `http://localhost:5000`.
3. **Artifact Logging**: Pipeline execution logs, Semgrep JSON findings, and ZAP HTML vulnerability reports are archived as build artifacts for compliance auditing.
