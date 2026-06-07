import os
import sys
import argparse
from jinja2 import Environment, FileSystemLoader

from gmail_html_tester.config import settings
from gmail_html_tester.generator import build_variants
from gmail_html_tester.mock import build_ai_mocks, build_mock_context
from gmail_html_tester.parser import (
    extract_for_loops,
    extract_if_flags,
    get_all_variables,
)
from gmail_html_tester.smtp import send_emails_bulk
from gmail_html_tester.utils import (
    Timer,
    print_banner,
    print_err,
    print_info,
    print_ok,
    print_section,
    print_summary,
    print_warn,
)


def _build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gmail-mailer",
        description="Smart HTML email template tester.",
    )
    p.add_argument(
        "template",
        nargs="?",
        default="templates/email_template.html",
        help="Path to a Jinja2 HTML template file.",
    )
    p.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Render variants to stdout without sending.",
    )
    return p


def _load_env_credentials():
    return (
        settings.sender_email,
        settings.app_password,
        settings.receiver_email,
        settings.use_gemini,
    )


def run(template_path: str | None = None, dry_run: bool = False) -> None:
    print_banner()
    if template_path is not None:
        target_template = template_path
        is_dry_run = dry_run
    else:
        args = _build_arg_parser().parse_args()
        target_template = args.template
        is_dry_run = args.dry_run

    sender, password, receiver, use_gemini = _load_env_credentials()

    if not is_dry_run and not all([sender, password, receiver]):
        print_err(
            "Missing .env values: "
            "SENDER_EMAIL, APP_PASSWORD, RECEIVER_EMAIL"
        )
        sys.exit(1)

    t_path = os.path.abspath(target_template)
    if not os.path.isfile(t_path):
        print_err(f"Template not found: {t_path}")
        sys.exit(1)

    t_dir = os.path.dirname(t_path)
    t_name = os.path.basename(t_path)

    env = Environment(
        loader=FileSystemLoader(t_dir),
        autoescape=False,
    )
    source = env.loader.get_source(env, t_name)[0]
    all_vars = get_all_variables(env, t_name)
    if_flags = extract_if_flags(source)
    for_loops = extract_for_loops(source)

    base_ctx = build_mock_context(all_vars, if_flags, for_loops)

    if use_gemini:
        scalar_vars = [
            v for v in all_vars
            if v not in {coll for _, coll in for_loops}
            and v not in {item for item, _ in for_loops}
            and v not in if_flags
        ]
        gemini_mocks = build_ai_mocks(
            scalar_vars,
            api_key=settings.gemini_api_key,
        )
        base_ctx.update(gemini_mocks)
    subject = f"[TEST] {t_name}"
    variants = build_variants(base_ctx, if_flags)

    print_section(f"Template: {t_name}")
    print_info(f"Variables : {len(all_vars)}")
    print_info(f"Flags     : {len(if_flags)}")
    print_info(f"Loops     : {len(for_loops)}")
    print_info(f"Variants  : {len(variants)}")

    if is_dry_run:
        print_warn("Dry-run mode — no emails will be sent")

    print_section("Dispatching")
    timer = Timer()
    total = len(variants)

    payloads = []
    for i, (label, ctx) in enumerate(variants, 1):
        v_subj = f"{subject} [{i}/{total}: {label}]"
        html = env.get_template(t_name).render(**ctx)
        if is_dry_run:
            print(f"\n--- VARIANT: {label} ---")
            print(f"Subject: {v_subj}")
            print(html)
            print("-" * 40)
        payloads.append((v_subj, html))

    errors = send_emails_bulk(
        sender,
        password,
        receiver,
        payloads,
        is_dry_run
    )

    sent = 0
    failed = 0
    for i, ((label, _), err) in enumerate(
        zip(variants, errors, strict=True), 1
    ):
        if err is None:
            print_ok(f"[{i}/{total}] {label}")
            sent += 1
        else:
            print_err(f"[{i}/{total}] {label} — {err}")
            failed += 1

    print_summary(sent, failed, timer.elapsed())
