# Application Threat Model & Data Flow Diagram (DFD)

## Data Flow Diagram (DFD)

[ User / Attacker ] ──( HTTP Request / Search Query )──> [ Web Server (Flask) ]
                                                                │
                                                    (Unsanitized SQL String)
                                                                ▼
                                                        [ SQLite Database ]

## STRIDE Threat Analysis

| Threat Category | Identified Vulnerability | Impact | Mitigation |
| :--- | :--- | :--- | :--- |
| **Spoofing** | Session token lack of secure flag | Session Hijacking | Enforce `Secure` and `HttpOnly` cookie flags |
| **Tampering** | SQL Injection in `/search` endpoint | Unauthorized DB read/write | Use Parameterized Queries (`cursor.execute("...", (query,))`) |
| **Repudiation** | Lack of centralized access logging | Inability to audit attacks | Implement structured JSON application logging |
| **Information Disclosure** | Verbose error stack traces returned to client | Architecture leakage | Disable Flask debug mode in production |
| **Elevation of Privilege** | Reflected XSS via `render_template_string` | Arbitrary JS execution | Use Jinja2 HTML auto-escaping templates |
