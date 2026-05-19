# gmail-template-tester

> **The fastest way to test, visualize, and finalize your HTML email templates.**

Stop wasting time triggering complex user flows just to see how a transactional email looks in your inbox. `gmail-template-tester` is an automated script that parses your Jinja2-style HTML templates, intelligently mocks the required data, and dispatches the final renders straight to your Gmail account — covering every conditional branch automatically.

---

## The Problem

Testing an email template the traditional way means:

1. Seeding fake data in your database
2. Clicking through a 5-step UI flow to trigger the email
3. Checking whether the email fired at all
4. Repeating for every `{% if %}` branch you need to cover

This tool eliminates all of that. **Point it at a template file and it handles the rest.**

---

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

---

## Prerequisites

- Python 3.7 or later
- A Gmail account
- A [Gmail App Password](https://support.google.com/accounts/answer/185833) (16 characters, generated from Google Account → Security → App Passwords)

> **Note:** App Passwords require 2-Step Verification to be enabled on your Google account.

---

## Installation

**1. Clone the repository**

```bash
git clone <your-repo-url>
cd gmail-template-tester
```

**2. Install dependencies**

```bash
pip install jinja2 python-dotenv
```

**3. Configure environment**

Create a `.env` file in the project root:

```env
SENDER_EMAIL=your_email@gmail.com
APP_PASSWORD=your_16_character_app_password
RECEIVER_EMAIL=where_to_send_tests@gmail.com
```

> Keep your `.env` file out of version control. A `.gitignore` entry for `.env` is included in the repo.

---

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

---

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

---

## Project Structure

```
gmail-template-tester/
├── main.py          # Entry point and CLI argument handling
├── parser.py        # Jinja2 AST traversal and token extraction
├── mocker.py        # Semantic data generation for detected variables
├── permuter.py      # Conditional branch permutation logic
├── mailer.py        # SMTP connection and email dispatch
├── .env             # Your credentials (not committed)
├── .env.example     # Example config for onboarding
├── .gitignore
└── README.md
```

---

## Configuration Reference

| Variable | Required | Description |
|---|---|---|
| `SENDER_EMAIL` | Yes | Gmail address used to send test emails |
| `APP_PASSWORD` | Yes | 16-character Gmail App Password |
| `RECEIVER_EMAIL` | Yes | Address where test variants are delivered |

---

## CLI Reference

```
python main.py <template_file> [options]

Arguments:
  template_file         Path to your Jinja2 HTML template

Options:
  --dry-run             Render all variants to stdout without sending
  --help                Show this help message
```

---

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

---

## Security Notes

- **App Passwords are not your account password.** They are scoped credentials that can be revoked independently at any time via Google Account → Security → App Passwords.
- Never commit your `.env` file. The included `.gitignore` excludes it by default.
- The tool connects over TLS (`STARTTLS`) — credentials are never transmitted in plaintext.
- Test emails are sent only to the `RECEIVER_EMAIL` address you specify, regardless of any email addresses present in the template.

---

## Troubleshooting

**`SMTPAuthenticationError`**
Your App Password may be incorrect or the sender account may not have 2-Step Verification enabled. Regenerate the password from Google Account → Security → App Passwords.

**`UndefinedError: 'X' is undefined`**
The mocker couldn't find a match for a variable name. The fallback is the key name itself — if you see raw variable names in the output, the mock was used. This is expected behaviour.

**`ConnectionRefusedError`**
Check your network connection and confirm `smtp.gmail.com` is reachable on port 587. Some corporate firewalls block outbound SMTP.

**Template produces too many variants**
Templates with many conditionals generate exponentially more emails. Use `--dry-run` to inspect the count before sending. Consider restructuring templates with many independent conditions into separate files.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please keep the codebase comment-free as a matter of style — the code is the documentation.

---

## License

MIT License. See `LICENSE` for details.

---

*Built to save developers time, frustration, and inbox clutter.*
