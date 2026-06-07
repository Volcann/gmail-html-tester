from .app import app
from . import tools


def run_server():
    app.run(transport="stdio")
