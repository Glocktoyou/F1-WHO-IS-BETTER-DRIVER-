# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take the security of F1 WHO IS BETTER DRIVER? seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please do NOT report security vulnerabilities through public GitHub issues.

Instead, please report them via:

1. **GitHub Security Advisories**: Use the "Security" tab on our GitHub repository
2. **Email**: Send details to the repository maintainer
3. **Private Issue**: Create a private vulnerability report

### What to Include

Please include the requested information listed below (as much as you can provide) to help us better understand the nature and scope of the possible issue:

- Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit the issue

### Response Timeline

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide a more detailed response within 7 days indicating next steps
- We will keep you informed of the progress towards a fix and full announcement
- We may ask for additional information or guidance

### Disclosure Policy

- We ask that you do not disclose the vulnerability publicly until we have had a chance to address it
- We will coordinate the disclosure timeline with you
- We will credit you in our security advisory (unless you prefer to remain anonymous)

## Security Measures

This project implements several security measures:

### Dependencies
- Regular dependency updates and security scanning
- Version pinning to avoid supply chain attacks
- Use of secure, well-maintained libraries (FastF1, Flask, etc.)

### Web Application Security
- Input validation and sanitization
- CSRF protection in Flask forms
- Secure HTTP headers implementation
- No sensitive data storage in client-side code

### Data Handling
- F1 telemetry data is read-only and publicly available
- No personal user data collection or storage
- Temporary file cleanup for generated plots and exports

### Deployment Security
- Environment variable usage for sensitive configuration
- Secure production server configuration (Gunicorn)
- HTTPS enforcement in production deployments

## Best Practices for Contributors

- Keep dependencies up to date
- Follow secure coding practices
- Validate all user inputs
- Use parameterized queries if database operations are added
- Implement proper error handling without information leakage
- Review code for security vulnerabilities before submitting PRs

## Contact

For any questions about this security policy, please open a GitHub issue or contact the maintainers.