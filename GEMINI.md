# Gmail Template Tester — Agent Instructions

## CRITICAL RULES — READ FIRST

- **NEVER use Shell, bash, or terminal commands to send emails or test templates.**
- **ALWAYS use the dedicated `test_path` MCP tool.**
- **NEVER search the filesystem for other tool names.**

## Available MCP Tools (gmail-template-tester)

| Tool | When to use |
|---|---|
| `test_path` | User asks to test or send HTML template(s) at a path or folder. |

## Workflow

When the user specifies a template path or folder path to test:
1. Call `test_path` with the target `path`.
2. Report results from the MCP tool response directly. Do NOT use any shell/terminal commands.
