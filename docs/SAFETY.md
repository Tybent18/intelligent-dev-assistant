# Safety and Authority

Obsidian Stage One is intentionally local and non-autonomous.

- Repository inspection is read-only.
- Python analysis uses parsing; it does not execute inspected project files.
- The command API exposes a fixed set of intents.
- Unknown commands produce suggestions rather than shell execution.
- Browser speech recognition depends on browser support and may use browser-vendor services.
- Speech synthesis is optional and remains inside the browser interface.
- No secrets, credentials, or source code are sent to an AI provider.
- No background monitoring or self-modification occurs.
- Human authorization remains required before any future file edit, command execution, deployment, or network action.

The visual interface is dramatic. Its authority is deliberately not.

