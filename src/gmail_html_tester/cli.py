import os
import sys
import argparse

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from gmail_html_tester.generator import build_variants
from gmail_html_tester.mock import build_mock_context
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
        default="email_template.html",
        help="Path to a Jinja2 HTML template file.",
    )
    p.add_argument(
        "--subject", "-s",
        default=None,
        metavar="TEXT",
        help="Override the email subject line.",
    )
    p.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Render variants to stdout without sending.",
    )
    p.add_argument(
        "--save-html",
        action="store_true",
        help="Write each rendered variant to disk.",
    )
    p.add_argument(
        "--list-vars",
        action="store_true",
        help="Print detected variables then exit.",
    )
    return p


def _load_env_credentials():
    load_dotenv()
    return (
        os.getenv("SENDER_EMAIL"),
        os.getenv("APP_PASSWORD"),
        os.getenv("RECEIVER_EMAIL"),
    )


def _save_variant(t_dir: str, stem: str, index: int, html: str) -> None:
    out = os.path.join(t_dir, f"{stem}_v{index}.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)


def run() -> None:
    print_banner()
    args = _build_arg_parser().parse_args()
    sender, password, receiver = _load_env_credentials()

    if not args.dry_run and not all([sender, password, receiver]):
        print_err(
            "Missing .env values: "
            "SENDER_EMAIL, APP_PASSWORD, RECEIVER_EMAIL"
        )
        sys.exit(1)

    t_path = os.path.abspath(args.template)
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

    if args.list_vars:
        print_section("Detected Variables")
        for v in sorted(all_vars):
            print_info(v)
        print_section("Conditional Flags")
        for f in if_flags:
            print_info(f)
        print_section("For-loop Collections")
        for item, coll in for_loops:
            print_info(f"{coll}  →  item: {item}")
        return

    base_ctx = build_mock_context(all_vars, if_flags, for_loops)
    subject = args.subject or f"[TEST] {t_name}"
    variants = build_variants(base_ctx, if_flags)
    stem = os.path.splitext(t_name)[0]

    print_section(f"Template: {t_name}")
    print_info(f"Variables : {len(all_vars)}")
    print_info(f"Flags     : {len(if_flags)}")
    print_info(f"Loops     : {len(for_loops)}")
    print_info(f"Variants  : {len(variants)}")

    if args.dry_run:
        print_warn("Dry-run mode — no emails will be sent")

    print_section("Dispatching")
    timer = Timer()
    total = len(variants)
    
    payloads = []
    for i, (label, ctx) in enumerate(variants, 1):
        v_subj = f"{subject} [{i}/{total}: {label}]"
        html = env.get_template(t_name).render(**ctx)
        if args.save_html:
            _save_variant(t_dir, stem, i, html)
        payloads.append((v_subj, html))
        
    errors = send_emails_bulk(sender, password, receiver, payloads, args.dry_run)
    
    sent = 0
    failed = 0
    for i, ((label, _), err) in enumerate(zip(variants, errors), 1):
        if err is None:
            print_ok(f"[{i}/{total}] {label}")
            sent += 1
        else:
            print_err(f"[{i}/{total}] {label} — {err}")
            failed += 1

    print_summary(sent, failed, timer.elapsed())
