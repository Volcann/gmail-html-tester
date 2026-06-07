import io
from contextlib import redirect_stdout, redirect_stderr

from .app import mcp
from gmail_html_tester.utils import get_html_templates
from gmail_html_tester.cli import run as run_main


@mcp.tool()
def test_path(path: str, dry_run: bool = False) -> str:
    templates = get_html_templates(path)
    if not templates:
        return f"Error: No HTML templates found at path '{path}'."

    results = []

    for tpl in sorted(templates):
        f = io.StringIO()
        with redirect_stdout(f), redirect_stderr(f):
            try:
                run_main(template_path=tpl, dry_run=dry_run)
            except SystemExit as e:
                if e.code != 0:
                    print(f"Process exited with code {e.code}")
            except Exception as e:
                print(f"Failed to process template: {e}")

        results.append(
            f"\n========================================\n"
            f"TEMPLATE: {tpl}\n"
            f"========================================\n"
            f"{f.getvalue()}"
        )

    return "\n".join(results)
