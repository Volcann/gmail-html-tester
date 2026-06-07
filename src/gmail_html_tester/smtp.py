import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

_SMTP_HOST = "smtp.gmail.com"
_SMTP_PORT = 587


def send_email(
    sender: str,
    app_password: str,
    receiver: str,
    subject: str,
    html_body: str,
    dry_run: bool = False,
) -> None:
    if dry_run:
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver
    msg.attach(MIMEText(html_body, "html", _charset="utf-8"))

    with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(sender, app_password)
        server.send_message(msg)


def send_emails_bulk(
    sender: str,
    app_password: str,
    receiver: str,
    payloads: list[tuple[str, str]],
    dry_run: bool = False,
) -> list[Exception | None]:
    if dry_run or not payloads:
        return [None] * len(payloads)

    results = []
    try:
        with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(sender, app_password)

            for subject, html_body in payloads:
                try:
                    msg = MIMEMultipart("alternative")
                    msg["Subject"] = subject
                    msg["From"] = sender
                    msg["To"] = receiver
                    msg.attach(MIMEText(html_body, "html", _charset="utf-8"))
                    server.send_message(msg)
                    results.append(None)
                except Exception as e:
                    results.append(e)
    except Exception as server_err:
        return [server_err] * len(payloads)

    return results
