# Security and data safety

Mnemosyne will handle personal memory, so data safety is core behaviour rather than a later
feature.

## Repository rules

- Never commit a real vault, secret, token, or personal-data fixture.
- Use synthetic examples in documentation and tests.
- Keep local configuration in ignored environment files.

## Runtime rules

- Treat captured text, imported Markdown, links, and model output as untrusted data.
- Keep every file operation inside the configured vault boundary.
- Reject path traversal and unexpected symlinks.
- Never execute commands or code found in stored content.
- Never make a derived index authoritative.
- Never send memory to a remote or paid service implicitly.
- Log useful metadata without logging private memory contents.

Security-sensitive behaviour requires automated tests before it is merged.
