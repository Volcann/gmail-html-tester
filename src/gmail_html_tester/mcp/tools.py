import os
import jinja2
from typing import Any

from .app import mcp
from .schemas import (
    AnalyzeReq,
    MockReq,
    DispatchReq,
    TestHtmlReq,
    UpdateTemplateReq,
    SyncAndTestReq,
)
from gmail_html_tester.parser import (
    extract_for_loops,
    extract_if_flags,
    get_all_variables,
)
from gmail_html_tester.mock import build_mock_context, get_mock_value, build_ai_mocks
from gmail_html_tester.config import settings
from gmail_html_tester.generator import build_variants
from gmail_html_tester.smtp import send_email, send_emails_bulk


@mcp.tool()
def analyze(req: AnalyzeReq) -> dict[str, Any]:
    path = os.path.join(os.getcwd(), "templates", req.tpl_name)

    if not os.path.exists(path):
        path = os.path.join(os.getcwd(), req.tpl_name)

    if not os.path.exists(path):
        return {"err": f"{req.tpl_name} not found."}

    t_dir = os.path.dirname(os.path.abspath(path))
    t_name = os.path.basename(path)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(t_dir))
    src = env.loader.get_source(env, t_name)[0]

    all_vars = get_all_variables(env, t_name)
    flags = extract_if_flags(src)
    loops = extract_for_loops(src)

    return {
        "ok": True,
        "vars": list(all_vars),
        "flags": flags,
        "loops": loops,
        "variants": 2 ** len(flags),
    }


@mcp.tool()
def generate_mocks(req: MockReq) -> dict[str, Any]:
    if req.use_gemini:
        return {"mocks": build_ai_mocks(req.vars, api_key=req.gemini_api_key or settings.gemini_api_key)}
    return {"mocks": {v: get_mock_value(v) for v in req.vars}}


@mcp.tool()
def dispatch(req: DispatchReq) -> dict[str, Any]:
    sender = os.getenv("SENDER_EMAIL")
    pwd = os.getenv("APP_PASSWORD")
    rcv = os.getenv("RECEIVER_EMAIL")

    path = os.path.join(os.getcwd(), "templates", req.tpl_name)
    if not os.path.exists(path):
        path = os.path.join(os.getcwd(), req.tpl_name)
    if not os.path.exists(path):
        return {"err": f"{req.tpl_name} not found."}

    with open(path, encoding="utf-8") as f:
        tpl_str = f.read()

    tpl = jinja2.Template(tpl_str)
    html = tpl.render(**req.mock_data)

    if req.dry_run:
        return {"ok": True, "preview": html[:500]}

    try:
        send_email(sender, pwd, rcv, f"[MCP] {req.tpl_name}", html, False)
        return {"ok": True, "rcv": rcv}
    except Exception as e:
        return {"err": str(e)}


@mcp.tool()
def test_raw_html(req: TestHtmlReq) -> dict[str, Any]:
    sender = os.getenv("SENDER_EMAIL")
    pwd = os.getenv("APP_PASSWORD")
    rcv = os.getenv("RECEIVER_EMAIL")

    if not req.dry_run and not all([sender, pwd, rcv]):
        return {"err": "Missing SMTP credentials."}

    env = jinja2.Environment()
    ast = env.parse(req.html)

    all_vars = jinja2.meta.find_undeclared_variables(ast)
    flags = extract_if_flags(req.html)
    loops = extract_for_loops(req.html)

    ctx = build_mock_context(all_vars, flags, loops)
    variants = build_variants(ctx, flags)
    tpl = env.from_string(req.html)

    payloads = []
    for label, c in variants:
        html = tpl.render(**c)
        subj = f"{req.subject} [{label}]"
        payloads.append((label, subj, html))

    res = []
    if req.dry_run:
        for label, subj, html in payloads:
            res.append({"label": label, "subj": subj, "preview": html[:200]})
    else:
        errors = send_emails_bulk(
            sender, pwd, rcv,
            [(subj, html) for _, subj, html in payloads],
            False
        )
        for (label, _, _), err in zip(payloads, errors, strict=False):
            if err is None:
                res.append({"label": label, "ok": True})
            else:
                res.append({"label": label, "err": str(err)})

    return {"ok": True, "total": len(variants), "res": res}


@mcp.tool()
def update_email_template(req: UpdateTemplateReq) -> dict[str, Any]:
    path = os.path.join(os.getcwd(), "templates", "email_template.html")

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(req.html)
        return {"ok": True, "path": path}
    except Exception as e:
        return {"err": str(e)}

@mcp.tool()
def sync_and_test_default_template(req: SyncAndTestReq) -> dict[str, Any]:
    path = os.path.join(os.getcwd(), "templates", "email_template.html")
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(req.html)

    test_req = TestHtmlReq(html=req.html, subject=req.subject, dry_run=False)
    return test_raw_html(test_req)
