import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

# load .env into os.environ
load_dotenv()

sender_email   = os.getenv("SENDER_EMAIL")
app_password   = os.getenv("APP_PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")

# Load your HTML template verbatim
with open("email_template.html", "r") as f:
    html_content = f.read()

# Build the HTML email
msg = MIMEText(html_content, "html", _charset="utf-8")
msg["Subject"] = "🚀 Live Gmail HTML Test"
msg["From"]    = sender_email
msg["To"]      = receiver_email

# Connect to Gmail SMTP
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.ehlo()
    server.starttls()
    server.login(sender_email, app_password)
    server.send_message(msg)

print("✅ Email sent—check your Gmail inbox now!")