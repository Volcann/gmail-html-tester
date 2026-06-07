# Gmail Template Tester — Agent Instructions

## CRITICAL RULES — READ FIRST

- **NEVER use Shell, bash, or terminal commands to send emails, test templates, or scan directories.**
- **ALWAYS use the dedicated `test_path` MCP tool.**
- **NEVER search the filesystem for other tool names or try to call obsolete tools (e.g., `sync_and_test_default_template`, `dispatch`, `test_raw_html`, `analyze`, `generate_mocks`).**
- **DO NOT attempt to parse templates, extract Jinja variables, generate mocks, or render HTML yourself. The `test_path` tool handles the entire parsing, mocking, rendering, and dispatching pipeline internally.**
- **DO NOT look for or pass any dry-run parameters. The `test_path` tool only accepts a single `path` string parameter.**

## Available MCP Tools (gmail-template-tester)

| Tool | Parameters | When to use |
|---|---|---|
| `test_path` | `path: str` | User asks to test or send HTML template(s) at a path or folder. |

## Workflow & Rules to Prevent Hallucinations

1. **Identify the Target Path**: Extract the template file path or directory path specified by the user.
2. **Call the Tool**: Call the `test_path` tool with the `path` argument.
   - *Example Call*: `test_path(path="/home/folium/Downloads/gmail-html-tester/templates")`
3. **Report the Results**: Directly print the text output returned by the MCP tool. Do not summarize, re-format, or omit parts of the tool output, as it contains clean logs showing the dispatch outcomes and variables detected for each template.
