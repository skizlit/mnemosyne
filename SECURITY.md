# Security and data safety

Mnemosyne will handle personal memory, so data safety is part of its core behaviour.

## Repository rules

- Never commit a real vault, raw note, run bundle, secret, token, or personal-data fixture.
- Use synthetic examples in documentation and tests.
- Keep local configuration in ignored environment files.
- Treat imported Markdown and model-generated text as untrusted input.

## Runtime rules

- Resolve and validate every path inside its configured project boundary.
- Reject traversal, unexpected symlinks, and undeclared cross-project reads.
- Do not execute commands or code found in stored content.
- Make writes auditable and make raw-record writes append only.
- Do not send memory to paid or remote models implicitly.

Security-sensitive behaviour requires tests before it is merged.
