<img src="https://user-images.githubusercontent.com/74038190/212284115-f47cd8ff-2ffb-4b04-b5bf-4d1c14c0247f.gif" width="100%">

## 🚀 Smart HTML Template Mailer

This tool allows you to take **any** HTML email template, automatically parse its Jinja2-style variables, and send it to your inbox to test how it renders. 

It acts as a robust testing engine for your email designs:
- **Auto-Detects Variables:** Finds all `{{ variable }}` instances and auto-generates logical dummy data based on the variable's name (e.g. `first_name` generates a real name, `url` generates a link).
- **Handles Conditional Logic:** Detects `{% if condition %}` blocks and automatically generates and sends multiple emails (one where the condition is True, one where it is False) to cover every scenario.
- **Supports Loops:** Identifies `{% for item in items %}` and automatically injects realistic JSON array data to test lists.
- **Modular and Clean Code:** Built strictly with flake8 standards across separate, organized modules.

<img src="https://user-images.githubusercontent.com/74038190/212284115-f47cd8ff-2ffb-4b04-b5bf-4d1c14c0247f.gif" width="100%">

### 🔧 Prerequisites

1. Python 3.7 or higher installed on your system.
2. A Gmail account with [App Password](https://support.google.com/accounts/answer/185833) enabled.
3. An HTML template utilizing Jinja2 template variables (like `demo_full_template.html`).

<img src="https://user-images.githubusercontent.com/74038190/212284115-f47cd8ff-2ffb-4b04-b5bf-4d1c14c0247f.gif" width="100%">

### 🔐 Generating a Gmail App Password

1. **Sign in to your Google Account** at [https://myaccount.google.com](https://myaccount.google.com).
2. Navigate to **Security** in the left sidebar.
3. Under **"Signing in to Google,"** enable **2-Step Verification** if you haven’t already.
4. Once 2-Step Verification is active, click **App passwords**.
5. Select **Mail** as the app and **Other (Custom name)** for the device, e.g., `PythonMailer`.
6. Click **Generate** and copy the 16‑character App Password.
7. Store this value in your `.env` under `APP_PASSWORD`.

### 🔑 Configuration Flow

1. **Clone or download** this repository to your local machine.

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install jinja2 python-dotenv
   ```

4. **Setup environment variables**:

   Create a file named `.env` in the project root.
   ```env
   SENDER_EMAIL=your@gmail.com
   APP_PASSWORD=16_character_app_password
   RECEIVER_EMAIL=recipient@gmail.com
   ```

### 🏃 How to Run

Simply execute the main orchestration file and pass the path to your HTML file:

```bash
python main.py demo_full_template.html
```

#### CLI Flags:
- `--subject` / `-s`: Specify the email subject manually.
- `--dry-run` / `-d`: Parse variables and render the templates locally without actually sending emails.
- `--save-html`: Output the final compiled templates as local HTML files (helpful for debugging).

### 💡 Project Architecture

The core code resides in the `mailer/` package to maintain separation of concerns and maximum cleanliness:
- `mailer/parser.py`: Scans templates and extracts variables, conditionals, and loops.
- `mailer/prompts.py`: Beautiful command-line interface to interactively gather values.
- `mailer/generator.py`: Permutation builder ensuring all `if`/`else` branches are tested.
- `mailer/smtp.py`: The secure dispatch interface for sending the built templates.
- `main.py`: The root script managing the flow of the application.

<img src="https://user-images.githubusercontent.com/74038190/212284115-f47cd8ff-2ffb-4b04-b5bf-4d1c14c0247f.gif" width="100%">

### 🤔 Troubleshooting

* **SMTP Timeout / Connection Errors**: Ensure port `587` is open, and your network allows outbound SMTP.
* **Authentication Failed**: Double-check your `APP_PASSWORD`. Regular Gmail passwords won’t work if 2FA is enabled.
* **Syntax Error in Template**: Make sure your `{% if %}` and `{% for %}` statements have proper terminating tags.
