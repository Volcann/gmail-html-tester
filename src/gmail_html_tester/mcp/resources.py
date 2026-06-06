import os
from .app import mcp


@mcp.resource("templates://{tpl_name}")
def get_tpl(tpl_name: str) -> str:
    path = os.path.join(os.getcwd(), "templates", tpl_name)

    if not os.path.exists(path):
        path = os.path.join(os.getcwd(), tpl_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{tpl_name} not found.")

    with open(path, encoding="utf-8") as f:
        return f.read()
