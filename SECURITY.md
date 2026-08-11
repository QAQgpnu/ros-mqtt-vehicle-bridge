# Security Policy

## Reporting

Please do not open a public issue for a suspected credential leak or exploitable vulnerability. Contact the maintainer privately through the email configured on the GitHub profile.

## Deployment guidance

- The bundled Mosquitto configuration is for localhost development only.
- Use TLS and authenticated accounts for production MQTT deployments.
- Inject credentials through a secret manager or process environment.
- Do not log credentials or production payloads.
- Rotate a credential immediately if it has ever been committed to Git.
