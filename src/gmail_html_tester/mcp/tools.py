import asyncio
import os
import sys

from .app import mcp
from gmail_html_tester.utils import get_html_templates


async def run_template_process(python_bin: str, main_py: str, tpl_path: str) -> str:
    process = await asyncio.create_subprocess_exec(
        python_bin,
        main_py,
        tpl_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    output = stdout.decode("utf-8", errors="replace")
    err_output = stderr.decode("utf-8", errors="replace")

    result = []
    if output:
        result.append(output)
    if err_output:
        result.append(err_output)
    if process.returncode != 0:
        result.append(f"Process exited with code {process.returncode}")

    return "\n".join(result)


@mcp.tool()
async def test_path(path: str) -> str:
    templates = get_html_templates(path)
    if not templates:
        return f"Error: No HTML templates found at path '{path}'."

    python_bin = sys.executable
    main_py = os.path.join(os.getcwd(), "main.py")

    tasks = [
        run_template_process(python_bin, main_py, tpl)
        for tpl in sorted(templates)
    ]
    outputs = await asyncio.gather(*tasks)

    results = []
    for tpl, out in zip(sorted(templates), outputs, strict=True):
        results.append(
            f"\n========================================\n"
            f"TEMPLATE: {tpl}\n"
            f"========================================\n"
            f"{out}"
        )

    return "\n".join(results)
