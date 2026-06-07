from . import tools  # noqa: F401
from .app import app


def run_server():
    app.run(transport="stdio")
