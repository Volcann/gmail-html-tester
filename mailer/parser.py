import re
from jinja2 import Environment, meta

IF_BLOCK_RE = re.compile(r'\{%-?\s*if\s+([^%]+?)\s*-?%\}', re.IGNORECASE)
FOR_BLOCK_RE = re.compile(
    r'\{%-?\s*for\s+(\w+)\s+in\s+(\w+)\s*-?%\}',
    re.IGNORECASE
)


def extract_if_flags(source: str) -> list[str]:
    flags = []
    for match in IF_BLOCK_RE.finditer(source):
        expr = match.group(1).strip()
        root = re.split(r'[\s=!<>.(]', expr.lstrip('not').strip())[0]
        if root and root.isidentifier() and root not in flags:
            flags.append(root)
    return flags


def extract_for_loops(source: str) -> list[tuple[str, str]]:
    loops = []
    for match in FOR_BLOCK_RE.finditer(source):
        item, collection = match.group(1), match.group(2)
        if (item, collection) not in loops:
            loops.append((item, collection))
    return loops


def get_all_variables(env: Environment, template_name: str) -> set[str]:
    source = env.loader.get_source(env, template_name)[0]
    ast = env.parse(source)
    return meta.find_undeclared_variables(ast)
