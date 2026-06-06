import re

from jinja2 import Environment, meta

IF_BLOCK_RE = re.compile(
    r'\{%-?\s*if\s+([^%]+?)\s*-?%\}',
    re.IGNORECASE,
)
FOR_BLOCK_RE = re.compile(
    r'\{%-?\s*for\s+(\w+)\s+in\s+(\w+)\s*-?%\}',
    re.IGNORECASE,
)

_JINJA_KEYWORDS = frozenset([
    "true", "false", "none", "null",
    "not", "and", "or", "in", "is",
    "loop", "super", "self",
])


def extract_if_flags(source: str) -> list:
    flags = []
    for match in IF_BLOCK_RE.finditer(source):
        expr = match.group(1).strip()
        expr = re.sub(r'^not\s+', '', expr, flags=re.IGNORECASE).strip()
        root = re.split(r'[\s=!<>.()\[\]]', expr)[0]
        if (
            root
            and root.isidentifier()
            and root not in _JINJA_KEYWORDS
            and root not in flags
        ):
            flags.append(root)
    return flags


def extract_for_loops(source: str) -> list:
    loops = []
    for match in FOR_BLOCK_RE.finditer(source):
        pair = (match.group(1), match.group(2))
        if pair not in loops:
            loops.append(pair)
    return loops


def get_all_variables(env: Environment, template_name: str) -> set:
    source = env.loader.get_source(env, template_name)[0]
    ast = env.parse(source)
    return meta.find_undeclared_variables(ast)
