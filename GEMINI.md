# Gmail Template Tester — Agent Instructions

## CRITICAL RULES — READ FIRST

- **NEVER use Shell, bash, or terminal commands to send emails or test templates.**
- **NEVER search the filesystem for tool names. All tools are MCP tools.**
- **ALWAYS call MCP tools directly. Do not look them up.**

## Available MCP Tools (gmail-template-tester)

| Tool | When to use |
|---|---|
| `sync_and_test_default_template` | User pastes HTML → save + send email immediately |
| `test_raw_html` | Test raw HTML without saving to disk |
| `analyze` | Inspect variables/flags in a template file |
| `generate_mocks` | Generate mock data for a list of variables |
| `dispatch` | Send a named template file with provided mock data |
| `update_email_template` | Save HTML to disk without sending |

## Workflow

When the user pastes HTML:
1. Call `sync_and_test_default_template` with the HTML directly.
2. Do NOT save to a new file. Do NOT use Shell.
3. Report results from the MCP tool response only.
