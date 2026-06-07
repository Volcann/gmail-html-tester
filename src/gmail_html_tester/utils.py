import os
import time

_RESET = "\033[0m"
_BOLD = "\033[1m"
_GREEN = "\033[92m"
_RED = "\033[91m"
_CYAN = "\033[96m"
_YELLOW = "\033[93m"
_DIM = "\033[2m"


def print_banner() -> None:
    print(_BOLD + "╔══════════════════════════════════════════╗" + _RESET)
    print(_BOLD + "║    🚀  Smart HTML Template Mailer        ║" + _RESET)
    print(_BOLD + "╚══════════════════════════════════════════╝" + _RESET)


def print_ok(msg: str) -> None:
    print(f"  {_GREEN}✔{_RESET}  {msg}")


def print_err(msg: str) -> None:
    print(f"  {_RED}✖{_RESET}  {msg}")


def print_info(msg: str) -> None:
    print(f"  {_CYAN}ℹ{_RESET}  {msg}")


def print_warn(msg: str) -> None:
    print(f"  {_YELLOW}⚠{_RESET}  {msg}")


def print_section(title: str) -> None:
    print(f"\n{_DIM}{'─' * 44}{_RESET}")
    print(f"  {_BOLD}{title}{_RESET}")
    print(f"{_DIM}{'─' * 44}{_RESET}")


def print_summary(sent: int, failed: int, elapsed: float) -> None:
    print()
    print(
        f"  {_BOLD}Result{_RESET}  "
        f"sent={_GREEN}{sent}{_RESET}  "
        f"failed={_RED}{failed}{_RESET}  "
        f"time={elapsed:.2f}s"
    )
    print()


class Timer:
    def __init__(self) -> None:
        self._start = time.monotonic()

    def elapsed(self) -> float:
        return time.monotonic() - self._start


def get_html_templates(path: str) -> list[str]:
    if os.path.isfile(path):
        if path.lower().endswith('.html'):
            return [path]
        return []

    if os.path.isdir(path):
        html_files = []
        for dirpath, _, filenames in os.walk(path):
            for file_name in filenames:
                if file_name.lower().endswith('.html'):
                    full_path = os.path.join(dirpath, file_name)
                    html_files.append(full_path)
        return html_files

    return []
