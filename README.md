# CF Authenticator

A JupyterHub authenticator for Cloudflare Zero Trust that enables secure authentication using Cloudflare Access JWT tokens.

## Overview

CF Authenticator is a custom authenticator for JupyterHub that integrates with Cloudflare Access to provide secure authentication. It validates JWT tokens issued by Cloudflare Access and uses the email address from the token as the username for JupyterHub sessions.

## Features

- Seamless integration with Cloudflare Access
- JWT token validation using Cloudflare's public signing keys
- Automatic user creation based on Cloudflare Access identity
- Configurable via environment variables
- Detailed logging for troubleshooting

## Installation

```bash
pip install cf_authenticator
```

## Configuration

1. Set up your Cloudflare Access application and note down your Team Domain and Application Audience (AUD) tag.

2. Configure the following environment variables:
   ```bash
   export POLICY_AUD="your-application-audience-tag"
   export TEAM_DOMAIN="https://your-team-domain.cloudflareaccess.com"
   ```

3. Configure JupyterHub to use the CF Authenticator by adding the following to your `jupyterhub_config.py`:
   ```python
   c.JupyterHub.authenticator_class = 'cf_authenticator.CFAuthenticator'
   ```

## How It Works

1. When a user accesses JupyterHub through Cloudflare Access, Cloudflare injects a JWT token in the request headers.
2. The authenticator validates this token using Cloudflare's public signing keys.
3. Upon successful validation, it extracts the user's email from the token.
4. The email is used as the username for the JupyterHub session.

## Development

To set up the development environment:

1. Clone the repository:
   ```bash
   git clone https://github.com/gcperformance/cf_authenticator.git
   cd cf_authenticator
   ```

2. Install development dependencies:
   ```bash
   pip install -e .
   ```

## Dependencies

- Python 3.6+
- PyJWT
- JupyterHub

## License

Apache License 2.0

## Author

Kyle Fletcher (kyle.fletcher@tbs-sct.gc.ca)
