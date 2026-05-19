import os
import sys
import argparse
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from mailer.parser import (
    extract_if_flags,
    extract_for_loops,
    get_all_variables,
)
from mailer.mock import build_mock_context
from mailer.generator import build_variants
from mailer.smtp import send_email


def main():
    print("╔══════════════════════════════════════════════╗")
    print("║      🚀 Smart HTML Template Mailer           ║")
    print("╚══════════════════════════════════════════════╝")

    parser = argparse.ArgumentParser(description="Smart HTML Mailer")
    parser.add_argument(
        "template",
        nargs="?",
        default="email_template.html"
    )
    parser.add_argument("--subject", "-s", default=None)
    parser.add_argument("--dry-run", "-d", action="store_true")
    parser.add_argument("--save-html", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    s_email = os.getenv("SENDER_EMAIL")
    a_pass = os.getenv("APP_PASSWORD")
    r_email = os.getenv("RECEIVER_EMAIL")

    if not args.dry_run and not all([s_email, a_pass, r_email]):
        print("Missing .env keys.")
        sys.exit(1)

    t_path = os.path.abspath(args.template)
    if not os.path.isfile(t_path):
        print(f"Template not found: {t_path}")
        sys.exit(1)

    t_dir = os.path.dirname(t_path)
    t_name = os.path.basename(t_path)

    env = Environment(loader=FileSystemLoader(t_dir), autoescape=False)
    source = env.loader.get_source(env, t_name)[0]
    all_vars = get_all_variables(env, t_name)
    if_flags = extract_if_flags(source)
    for_loops = extract_for_loops(source)

    base_ctx = build_mock_context(all_vars, if_flags, for_loops)

    subj = args.subject or f"Test {t_name}"
    variants = build_variants(base_ctx, if_flags)

    sent = 0
    failed = 0

    for i, (label, ctx) in enumerate(variants, 1):
        v_subj = f"{subj} [{i}/{len(variants)}: {label}]"
        try:
            html = env.get_template(t_name).render(**ctx)
            if args.save_html:
                out_name = f"{os.path.splitext(t_name)[0]}_v{i}.html"
                with open(os.path.join(t_dir, out_name), "w") as f:
                    f.write(html)
            send_email(s_email, a_pass, r_email, v_subj, html, args.dry_run)
            sent += 1
        except Exception as e:
            print(f"Error: {e}")
            failed += 1

    print(f"\nDone. Sent: {sent}, Failed: {failed}")


if __name__ == "__main__":
    main()
