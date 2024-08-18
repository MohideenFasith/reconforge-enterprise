# Security Policy

## Supported version

Security fixes are applied to the current main branch.

## Reporting

Report suspected vulnerabilities privately to the repository owner. Do not include live customer credentials, financial records, or secrets in public issues.

## Security design

Authentication uses configured API keys mapped to a principal, tenant, and roles. Administrative endpoints require the `admin` role. Tenant identifiers are derived from authentication and are not accepted from request bodies.

Webhook secrets are used only to produce HMAC signatures and are not included in delivery payloads. Production webhook URLs must use HTTPS.

Secrets belong in environment variables or a secret manager. `.env` is ignored by Git and `.env.example` contains only non-secret examples.

CI performs dependency auditing and a fresh container smoke test. Docker runs as a non-root user and Compose enables a read-only filesystem and `no-new-privileges`.
