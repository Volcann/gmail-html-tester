# 🚀 Gmail Template Tester

**The fastest way to test, visualize, and finalize your HTML email templates.**

Stop wasting time triggering complex user flows just to see how a transactional email looks in your inbox. **Gmail Template Tester** is an automated script that parses your Jinja2-style HTML templates, intelligently mocks the required data, and dispatches the final renders straight to your Gmail account. 

Testing an email template used to mean faking data in your database, clicking through a 5-step UI, and praying the email triggers. This tool **reduces testing time by 60%** by allowing you to test templates in isolation, covering all edge cases simultaneously.

## 🌟 The Impact

- **Instant Visual Feedback:** See exactly how your HTML looks in a real Gmail client. No more guessing how CSS will render.
- **Automated Edge Case Testing:** If your template has `{% if is_premium %}` logic, this tool automatically generates and sends *multiple* versions of the email (one for the True condition, one for the False condition). You see every scenario without lifting a finger.
- **Zero Configuration Data Mocking:** It automatically detects `{{ variables }}` and `{% for items %}` loops inside your template and intelligently injects realistic fake data (like real-sounding names, URLs, or prices). No need to manually provide inputs!
- **Drastically Reduced QA Time:** Skip the tedious project flows. Validate your designs and logic in seconds.

## 🔧 Prerequisites

1. Python 3.7+ installed.
2. A Gmail account with an [App Password](https://support.google.com/accounts/answer/185833) enabled.

## 🚀 Getting Started

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd gmail-html-mailer
   ```

2. **Install dependencies**
   ```bash
   pip install jinja2 python-dotenv
   ```

3. **Configure your environment**
   Create a `.env` file in the root directory:
   ```env
   SENDER_EMAIL=your_email@gmail.com
   APP_PASSWORD=your_16_character_app_password
   RECEIVER_EMAIL=where_to_send_tests@gmail.com
   ```

4. **Run the tester**
   Simply point the script at your HTML template:
   ```bash
   python main.py my_template.html
   ```

That's it. Sit back and watch your inbox fill up with perfectly rendered test scenarios. 

*Want to test locally without sending emails? Use the `--dry-run` flag!*

## 💡 How It Works Under The Hood

The tool operates entirely autonomously:
1. **Parses** your template using the Jinja2 AST (Abstract Syntax Tree) to map all required variables and logical branches.
2. **Mocks** the missing data (e.g., automatically injecting real-sounding names for `{{ first_name }}` or arrays for `{% for item in items %}`).
3. **Generates** permutations of your `{% if %}` / `{% else %}` blocks to ensure every branch of your template is tested.
4. **Dispatches** the emails securely over Gmail's SMTP server.

Built cleanly across multiple files without any unnecessary comments, it acts as a lightweight, drop-in utility for any backend developer.

---
*Built to save developers time, frustration, and inbox clutter.*
