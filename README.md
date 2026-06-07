<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/7/7e/Gmail_icon_%282020%29.svg" width="128" height="128" alt="Gmail Logo">
</p>

<h1 align="center">
  🚀 Gmail Template Tester
</h1>
<h4 align="center">
  The fastest way to test, visualize, and finalize your HTML email templates.
</h4>

<p align="center">
  <a href="#license">
    <img alt="License" src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge&color=B5E8E0&logoColor=D9E0EE&labelColor=302D41">
  </a>
  <a href="https://github.com/Volcann/gmail-html-mailer/stargazers">
    <img alt="Stargazers" src="https://img.shields.io/github/stars/volcann/gmail-html-mailer?style=for-the-badge&logo=starship&color=B5E8E0&logoColor=D9E0EE&labelColor=302D41">
  </a>
  <a href="https://github.com/Volcann/gmail-html-mailer/graphs/contributors">
    <img alt="Contributors" src="https://img.shields.io/github/contributors/volcann/gmail-html-mailer?style=for-the-badge&logo=gitbook&color=B5E8E0&logoColor=D9E0EE&labelColor=302D41">
  </a>
</p>

Stop wasting time triggering complex user flows just to see how a transactional email looks in your inbox. `gmail-template-tester` is an automated script that parses your Jinja2-style HTML templates, intelligently mocks the required data, and dispatches the final renders straight to your Gmail account — covering every conditional branch automatically.

Now with **Gemini CLI integration**: pass template paths directly from your terminal in plain English and fire tests to your inbox without touching the Python script manually. Gemini CLI uses token caching to reduce API overhead, keeping your workflow lean.

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## The Problem

Testing an email template the traditional way means:

1. Seeding fake data in your database
2. Clicking through a 5-step UI flow to trigger the email
3. Checking whether the email fired at all
4. Repeating for every `{% if %}` branch you need to cover

This tool eliminates all of that. **Point it at a template file and it handles the rest.**

## Impact

| Metric | Before | After |
|---|---|---|
| Time to test a single template | ~15 min | ~5 sec |
| Branches covered per run | 1 (manual) | All (automatic) |
| Database setup required | Yes | No |
| UI flow required | Yes | No |

- **Instant visual feedback** — see exactly how your HTML renders in a real Gmail client
- **Automated branch coverage** — every `{% if is_premium %}` produces a separate email automatically
- **Zero-configuration mocking** — `{{ first_name }}` gets a real-sounding name; `{{ price }}` gets a realistic price
- **60% reduction in QA time** for email template validation
- **Gemini CLI shortcut** — describe your template path in plain English and let Gemini dispatch the test

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## ⚡ Choose Your Mode

> Pick the workflow that fits you. Both modes do the same thing — send rendered email variants straight to your inbox.

<table>
<tr>
<td width="50%" align="center">

### 🐍 Without Gemini CLI

```bash
python main.py templates/welcome.html
python main.py templates/invoice.html --dry-run
```

➡️ [Jump to Python Usage](#usage)

</td>
<td width="50%" align="center">

### 🤖 With Gemini CLI

```
> Test templates/welcome.html and send to my inbox
> Dry-run all templates in the templates/ folder
```

➡️ [Jump to Gemini CLI Setup](#gemini-cli-integration)

</td>
</tr>
</table>

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## 📑 Navigation
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage) *(Python CLI)*
- [Gemini CLI Integration](#gemini-cli-integration)
- [Console Output](#console-output)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Configuration Reference](#configuration-reference)
- [CLI Reference](#cli-reference)
- [Template Compatibility](#template-compatibility)
- [Security Notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## Prerequisites

- Python 3.7 or later
- A Gmail account
- A [Gmail App Password](https://support.google.com/accounts/answer/185833) (16 characters, generated from Google Account → Security → App Passwords)
- *(Optional)* [Gemini CLI](https://github.com/google-gemini/gemini-cli) for natural-language template dispatching

> **Note:** App Passwords require 2-Step Verification to be enabled on your Google account.

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/Volcann/gmail-html-mailer.git
cd gmail-html-mailer
```

**2. Install dependencies**

```bash
# Using uv (recommended)
uv sync

# Or using standard python venv + pip
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

**3. Configure environment**

Create a `.env` file in the project root:

```env# SMTP Configuration
SENDER_EMAIL=your_email@gmail.com
APP_PASSWORD=your_16_character_app_password
RECEIVER_EMAIL=where_to_send_tests@gmail.com

# LLM Context Generation (Optional)
USE_GEMINI=false
GEMINI_API_KEY=your_gemini_api_key_here
```

> Keep your `.env` file out of version control. A `.gitignore` entry for `.env` is included in the repo.

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## Usage

**Basic usage**

```bash
python main.py my_template.html
```

**Preview without sending (dry-run)**

```bash
python main.py my_template.html --dry-run
```

Dry-run mode renders every variant to stdout without touching SMTP. Use it for local review, CI checks, or when you want to inspect the mocked data before sending.

**Examples**

```bash
# Test a welcome email
python main.py templates/welcome.html

# Test an invoice template in dry-run mode
python main.py templates/invoice.html --dry-run

# Test a notification email
python main.py templates/order_shipped.html
```

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## Console Output

```text
╔══════════════════════════════════════════╗
║    🚀  Smart HTML Template Mailer        ║
╚══════════════════════════════════════════╝

────────────────────────────────────────────
  Template: demo_template.html
────────────────────────────────────────────
  ℹ  Variables : 19
  ℹ  Flags     : 2
  ℹ  Loops     : 1
  ℹ  Variants  : 4
  ⚠  Dry-run mode — no emails will be sent

────────────────────────────────────────────
  Dispatching
────────────────────────────────────────────
  ✔  [1/4] ON:is_premium+show_banner
  ✔  [2/4] ON:is_premium | OFF:show_banner
  ✔  [3/4] ON:show_banner | OFF:is_premium
  ✔  [4/4] OFF:is_premium+show_banner

  Result  sent=4  failed=0  time=0.01s
```

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## Gemini CLI Integration

You can drive this tool from [Gemini CLI](https://github.com/google-gemini/gemini-cli) — Google's open-source terminal AI agent — instead of invoking Python directly. This is useful when you want to test multiple templates in one go, or when you prefer a conversational interface over remembering CLI flags.

**Why Gemini CLI?**

Gemini CLI runs on Gemini 2.5 Pro with a 1M token context window and uses automatic token caching to avoid re-processing repeated context on every call. For a script like this — where you're firing the same setup repeatedly across different templates — that caching keeps things fast and cheap.

**Install Gemini CLI**

```bash
npm install -g @google/gemini-cli
# or run without installing:
npx @google/gemini-cli
```

**Example prompts**

Once inside a Gemini CLI session in your project directory:

```
> Test templates/welcome.html and send it to my inbox
> Run a dry-run on templates/invoice.html and show me the output
> Test all templates in the templates/ folder
```

Gemini CLI will resolve the template paths, run `main.py` with the appropriate arguments, and report back results — all without you writing a single command manually.

**Headless / scripted usage**

```bash
echo "Test templates/order_shipped.html" | gemini --yolo
```

The `--yolo` flag lets Gemini execute shell commands without prompting for confirmation — suitable for CI pipelines.

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## How It Works

The tool operates in four autonomous stages:

### 1. Parse the AST

Uses the Jinja2 Abstract Syntax Tree to map every token in your template:

- `{{ variable }}` — identifies all required variables
- `{% if condition %}` — identifies all conditional branches
- `{% for item in items %}` — identifies all loops

### 2. Mock the data

Generates semantically plausible fake data for every variable detected:

| Variable pattern | Generated value |
|---|---|
| `first_name`, `last_name`, `name` | Real-sounding full names |
| `email` | Realistic email addresses |
| `price`, `amount`, `cost` | Formatted currency values |
| `url`, `link` | Valid HTTPS URLs |
| `date`, `timestamp` | Formatted date strings |
| `{% for item in items %}` | Arrays of 2–4 realistic items |
| Anything else | Title-cased key name as fallback |

### 3. Generate permutations

For every `{% if %}`/`{% else %}` block detected, the tool generates a separate render with that condition set to `True` and another with it set to `False`.

A template with **2 conditionals** produces **4 emails** (2² = 4).
A template with **3 conditionals** produces **8 emails** (2³ = 8).

Every branch is covered. Nothing hides.

### 4. Dispatch via SMTP

Fires each rendered variant over Gmail's SMTP server (`smtp.gmail.com:587`) using TLS and your App Password. All sends are logged to stdout with timing information.

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## Project Structure
```
gmail-html-tester/
├── src/
│   └── gmail_html_tester/
│       ├── **init**.py
│       ├── cli.py             # Entry point and CLI argument parsing
│       ├── config.py          # Configuration loading and management
│       ├── generator.py       # Data generation engine
│       ├── parser.py          # Jinja2 AST traversal and token extraction
│       ├── smtp.py            # SMTP connection and email dispatching
│       ├── utils.py           # Core shared utility functions
│       ├── mcp/               # Model Context Protocol (MCP) integration
│       │   ├── **init**.py
│       │   ├── app.py         # MCP application initialization
│       │   ├── server.py      # MCP server core logic
│       │   └── tools.py       # LLM-facing tool definitions
│       └── mock/              # Mocking data engine
│           ├── **init**.py
│           ├── constants.py   # Fallback schemas and semantic constants
│           ├── mocks.py       # Faker data generation logic
│           └── utils.py       # Mocking helper functions
├── templates/
│   └── email_template.html    # Reference/sample HTML email template
├── tests/                     # Unit and integration tests
├── GEMINI.md                  # LLM context / instruction guide
├── LICENSE                    # Project license
├── main.py                    # Root script convenience entry point
├── mcp_server.py              # Dedicated entry point for the MCP server
├── pyproject.toml             # Project metadata and dependencies (PEP 621)
├── README.md                  # Project documentation
└── uv.lock                    # Locked dependency tree managed by uv

```

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## Configuration Reference

The application relies on environment variables for authentication, SMTP routing, and LLM features. Create a `.env` file in the root directory based on the reference below:

### Environment Variables

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `SENDER_EMAIL` | **Yes** | *None* | The Gmail address used to dispatch test emails. |
| `APP_PASSWORD` | **Yes** | *None* | A 16-character Google App Password (not your standard password). |
| `RECEIVER_EMAIL` | **Yes** | *None* | The destination address where test email variants are delivered. |
| `USE_GEMINI` | No | `false` | Set to `true` to enable LLM-powered context generation for templates. |
| `GEMINI_API_KEY` | No* | *None* | API key for Gemini. *Required if `USE_GEMINI` is set to `true`*. |

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## CLI Reference

```
python main.py <template_file> [options]

Arguments:
  template_file         Path to your Jinja2 HTML template

Options:
  --dry-run             Render all variants to stdout without sending
  --help                Show this help message
```

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## Template Compatibility

The tool supports standard Jinja2 syntax:

```html
<!-- Variables -->
Hello {{ first_name }},

<!-- Conditionals -->
{% if is_premium %}
  <p>Your premium plan renews on {{ renewal_date }}.</p>
{% else %}
  <p><a href="{{ upgrade_url }}">Upgrade to Premium →</a></p>
{% endif %}

<!-- Loops -->
{% for item in order_items %}
  <tr>
    <td>{{ item.name }}</td>
    <td>{{ item.price }}</td>
  </tr>
{% endfor %}
```

> Nested conditionals and nested loops are supported. Each nesting level compounds the permutation count, so templates with 4+ conditionals may produce a large number of variants. Use `--dry-run` to preview first.

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## Security Notes

- **App Passwords are not your account password.** They are scoped credentials that can be revoked independently at any time via Google Account → Security → App Passwords.
- Never commit your `.env` file. The included `.gitignore` excludes it by default.
- The tool connects over TLS (`STARTTLS`) — credentials are never transmitted in plaintext.
- Test emails are sent only to the `RECEIVER_EMAIL` address you specify, regardless of any email addresses present in the template.

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## Troubleshooting

**`SMTPAuthenticationError`**
Your App Password may be incorrect or the sender account may not have 2-Step Verification enabled. Regenerate the password from Google Account → Security → App Passwords.

**`UndefinedError: 'X' is undefined`**
The mocker couldn't find a match for a variable name. The fallback is the key name itself — if you see raw variable names in the output, the mock was used. This is expected behaviour.

**`ConnectionRefusedError`**
Check your network connection and confirm `smtp.gmail.com` is reachable on port 587. Some corporate firewalls block outbound SMTP.

**Template produces too many variants**
Templates with many conditionals generate exponentially more emails. Use `--dry-run` to inspect the count before sending. Consider restructuring templates with many independent conditions into separate files.

**Gemini CLI not running the script correctly**
Make sure you're running the Gemini CLI session from inside the project directory so it can resolve relative template paths. If Gemini halts before executing, add `--yolo` to skip confirmation prompts.

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please keep the codebase comment-free as a matter of style — the code is the documentation.

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

## License

MIT License. See `LICENSE` for details.

<img src="https://img.shields.io/badge/-007ACC?style=flat&line-height=1&width=1000" width="100%" height="3px">

*Built to save developers time, frustration, and inbox clutter.*
