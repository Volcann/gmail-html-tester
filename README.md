## 🚀 Send mails to Gmail in seconds

This guide walks you through configuring and running a simple Python script to send HTML emails via Gmail SMTP in just a few seconds. Perfect for quick notifications, alerts, or any automated email tasks.

---

### 🔧 Prerequisites

1. Python 3.7 or higher installed on your system.
2. A Gmail account with [App Password](https://support.google.com/accounts/answer/185833) enabled (recommended for security).
3. Basic familiarity with the terminal/command line.
4. Your HTML email template (`email_template.html`).

---

### 🔑 Configuration Flow

1. **Clone or download** this repository to your local machine.

   ```bash
   git clone https://github.com/your-username/gmail-html-mailer.git
   cd gmail-html-mailer
   ```

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\\Scripts\\activate  # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**:

   * Create a file named `.env` in the project root.
   * Add the following keys, replacing values with your own credentials:

     ```env
     SENDER_EMAIL=your@gmail.com
     APP_PASSWORD=16_character_app_password
     RECEIVER_EMAIL=recipient@gmail.com
     ```

5. **Prepare your HTML template**:

   * Ensure there’s a file named `email_template.html` in the root.
   * Add any inline styles, images, or structure you need.

6. **Run the script**:

   ```bash
   python send_html_email.py
   ```

   You should see `✅ Email sent—check your Gmail inbox now!` in your console.

---

### 💡 How It Works

1. **Load `.env`**: The script uses `python-dotenv` to load credentials into `os.environ`.
2. **Read HTML Template**: Pulls in your `email_template.html` verbatim.
3. **Compose Email**: Uses `email.mime.text.MIMEText` to wrap the HTML content.
4. **Connect & Authenticate**: Opens an SMTP connection to `smtp.gmail.com:587`, starts TLS, and logs in.
5. **Send**: Dispatches the email and closes the connection automatically.

---

### 🤔 Troubleshooting

* **SMTP Timeout / Connection Errors**: Ensure port `587` is open, and your network allows outbound SMTP.
* **Authentication Failed**: Double-check your `APP_PASSWORD`. Regular Gmail passwords won’t work if 2FA is enabled.
* **HTML Not Rendering**: Confirm your template is valid HTML and includes proper `<html>`, `<body>`, etc.

---

### 📈 Next Steps

* Integrate into a larger notification system or CI/CD pipeline.
* Swap Gmail SMTP for another provider (Outlook, SendGrid, etc.).
* Expand to include attachments, inline images, or templating engines like Jinja2.
