from .app import mcp


def run_server():
    mcp.run(transport="stdio")
