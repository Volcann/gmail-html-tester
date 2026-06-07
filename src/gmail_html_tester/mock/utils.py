import random
import string
from datetime import datetime, timedelta

from .constants import (
    BADGE_LABELS, BASE_URLS, CATEGORIES, CITIES, COMPANIES,
    CTA_TEXTS, CURRENCIES, DOMAINS, FIRST_NAMES, LAST_NAMES,
    PLAN_NAMES, PRODUCTS, ROLES, SCHOOLS, STATUSES, SUPPORT_EMAILS,
)


def order_id() -> str:
    return f"ORD-{random.randint(100000, 999999)}"


def invoice_id() -> str:
    return f"INV-{random.randint(2024100, 2024999)}"


def ticket_id() -> str:
    return f"TKT-{random.randint(10000, 99999)}"


def promo_code() -> str:
    return f"SAVE{random.randint(10, 50)}"


def token() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=32))


def url(path_key: str = "dashboard") -> str:
    base = random.choice(BASE_URLS)
    paths = {
        "login":      "/auth/login",
        "signup":     "/auth/register",
        "dashboard":  "/dashboard",
        "settings":   "/settings/profile",
        "billing":    "/settings/billing",
        "upgrade":    "/upgrade?ref=email",
        "confirm":    f"/confirm?token={token()}",
        "reset":      f"/auth/reset-password?token={token()}",
        "unsubscribe": f"/unsubscribe?uid={token()[:16]}",
        "invoice":    f"/invoices/{invoice_id()}",
        "order":      f"/orders/{order_id()}",
        "track":      f"/shipping/track?id={order_id()}",
        "profile":    "/profile/edit",
        "help":       "/help",
        "privacy":    "/legal/privacy",
        "terms":      "/legal/terms",
    }
    return base + paths.get(path_key, "/")


def date(offset_days: int = 0, fmt: str = "%B %d, %Y") -> str:
    return (datetime.now() + timedelta(days=offset_days)).strftime(fmt)


def email(first: str = "", last: str = "") -> str:
    domain = random.choice(DOMAINS)
    if first and last:
        return f"{first.lower()}.{last.lower()}@{domain}"
    return f"user{random.randint(1000, 9999)}@{domain}"


def price() -> str:
    currency = random.choice(CURRENCIES)
    amounts = [9.99, 19.99, 29.99, 49.99, 79.99, 99.99, 149.00, 299.00]
    amount = random.choice(amounts)
    return f"{currency}{amount:,.2f}"


def full_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def get_mock_value(var_name: str) -> str:
    n = var_name.lower().replace(".", "_")

    if any(x in n for x in ["first_name", "firstname"]):
        return random.choice(FIRST_NAMES)
    if any(x in n for x in ["last_name", "lastname", "surname"]):
        return random.choice(LAST_NAMES)
    if any(x in n for x in ["full_name", "fullname", "student_name", "student"]):
        return full_name()
    if any(x in n for x in ["username", "user_name", "handle"]):
        return f"{random.choice(FIRST_NAMES).lower()}{random.randint(10, 99)}"
    if "name" in n:
        return full_name()

    if "support_email" in n:
        return random.choice(SUPPORT_EMAILS)
    if any(x in n for x in ["email", "mail_address"]):
        return email(random.choice(FIRST_NAMES), random.choice(LAST_NAMES))

    _url_map = {
        "unsubscribe": ["unsubscribe_url", "unsubscribe_link"],
        "login":       ["login_url", "signin_url", "sign_in_url"],
        "signup":      ["signup_url", "register_url"],
        "dashboard":   [
            "dashboard_url",
            "dashboard_link",
            "cta_url",
            "action_url",
            "button_url"
        ],
        "billing":     ["billing_url", "billing_link"],
        "upgrade":     ["upgrade_url", "upgrade_link"],
        "confirm":     [
            "confirm_url",
            "confirmation_url", "verify_url", "verification_url"
        ],
        "reset":       ["reset_url", "reset_link", "password_reset"],
        "invoice":     ["invoice_url", "invoice_link"],
        "order":       ["order_url", "order_link"],
        "track":       ["track_url", "tracking_url", "tracking_link"],
        "profile":     ["profile_url", "profile_link"],
        "help":        ["help_url", "help_link", "support_url"],
        "privacy":     ["privacy_url", "privacy_link"],
        "terms":       ["terms_url", "terms_link"],
    }
    for path_key, patterns in _url_map.items():
        if any(x in n for x in patterns):
            return url(path_key)
    if any(x in n for x in ["url", "link", "href"]):
        return url("dashboard")

    if any(x in n for x in [
        "company_name", "company", "org_name", "organisation", "organization"
    ]):
        return random.choice(COMPANIES)
    if "school" in n:
        return random.choice(SCHOOLS)
    if "brand" in n:
        return random.choice(COMPANIES)

    if any(x in n for x in [
        "price", "amount", "cost", "total", "subtotal",
        "tax", "fee", "charge", "balance", "refund",
        "discount_amount", "savings", "plan_price",
        "monthly_price", "annual_price"
    ]):
        return price()

    if any(x in n for x in ["plan_name", "plan", "tier", "subscription"]):
        return random.choice(PLAN_NAMES)
    if "billing_cycle" in n:
        return random.choice(["Monthly", "Annual"])
    if any(x in n for x in ["seats", "seat_count"]):
        return str(random.randint(2, 25))

    if any(x in n for x in ["order_id", "order_number"]):
        return order_id()
    if any(x in n for x in ["invoice_id", "invoice_number"]):
        return invoice_id()
    if any(x in n for x in ["ticket_id", "ticket_number", "ticket"]):
        return ticket_id()
    if any(x in n for x in ["promo_code", "coupon", "discount_code", "voucher"]):
        return promo_code()
    if any(x in n for x in ["token", "api_key", "secret", "verification_code"]):
        return token()
    if any(x in n for x in ["transaction_id", "payment_id"]):
        chars = string.ascii_uppercase + string.digits
        return f"TXN-{''.join(random.choices(chars, k=12))}"

    if any(x in n for x in ["renewal_date", "next_billing_date", "next_charge_date"]):
        return date(offset_days=random.randint(1, 30))
    if any(x in n for x in ["expiry_date", "expiration_date", "expires_at"]):
        return date(offset_days=random.randint(3, 14))
    if any(x in n for x in ["due_date", "payment_due"]):
        return date(offset_days=random.randint(7, 30))
    if any(x in n for x in ["date", "created_at", "updated_at", "timestamp"]):
        return date()
    if "year" in n:
        return str(datetime.now().year)
    if "time" in n:
        return datetime.now().strftime("%I:%M %p")

    if any(x in n for x in ["address", "city", "location"]):
        return random.choice(CITIES)
    if "country" in n:
        countries = ["United States", "United Kingdom", "Canada", "Australia"]
        return random.choice(countries)
    if any(x in n for x in ["postal_code", "zip_code", "zipcode"]):
        return str(random.randint(10000, 99999))

    if any(x in n for x in ["role", "permission", "access_level"]):
        return random.choice(ROLES)
    if "department" in n:
        departments = ["Engineering", "Marketing", "Sales", "Support", "Design"]
        return random.choice(departments)

    if any(x in n for x in ["status", "state", "order_status", "payment_status"]):
        return random.choice(STATUSES)
    if any(x in n for x in ["badge", "badge_label", "label"]):
        return random.choice(BADGE_LABELS)

    if any(x in n for x in ["product_name", "item_name", "product"]):
        return random.choice(PRODUCTS)
    if "category" in n:
        return random.choice(CATEGORIES)
    if any(x in n for x in ["quantity", "qty"]):
        return str(random.randint(1, 10))
    if "sku" in n:
        chars = string.ascii_uppercase + string.digits
        return f"SKU-{''.join(random.choices(chars, k=8))}"

    if any(x in n for x in ["cta_text", "button_text", "button_label", "action_label"]):
        return random.choice(CTA_TEXTS)

    if any(x in n for x in ["subject", "email_subject"]):
        return random.choice([
            "Your order is confirmed",
            "Welcome aboard — let's get started",
            "Action required on your account",
        ])
    if any(x in n for x in ["title", "heading", "headline"]):
        return random.choice([
            "Welcome to the Platform", "Your Account Has Been Created",
            "Order Confirmed", "Invoice Ready",
        ])
    if any(x in n for x in [
        "message", "body", "content", "intro", "description", "desc"
    ]):
        return random.choice([
            "We're excited to have you on board. Everything is set up.",
            "A quick heads-up about your account — please review the details.",
            "Your request has been processed successfully.",
        ])
    if any(x in n for x in ["tagline", "subtitle", "subheading"]):
        return "Simple, powerful, and built for teams."
    if any(x in n for x in ["note", "footnote", "footer_note"]):
        return "This is an automated message. Please do not reply."
    if any(x in n for x in ["greeting", "salutation"]):
        return f"Hello, {random.choice(FIRST_NAMES)}!"
    if any(x in n for x in ["signature", "sign_off"]):
        return f"The {random.choice(COMPANIES)} Team"

    if any(x in n for x in ["count", "total_count", "num", "number"]):
        return str(random.randint(1, 50))
    if any(x in n for x in ["percentage", "percent", "rate"]):
        return f"{random.randint(5, 40)}%"
    if any(x in n for x in ["days_left", "days_remaining", "days_until"]):
        return str(random.randint(1, 30))
    if any(x in n for x in ["phone", "phone_number", "mobile"]):
        return (
            f"+1 ({random.randint(200, 999)}) "
            f"{random.randint(200, 999)}-{random.randint(1000, 9999)}"
        )

    return f"Sample {var_name.replace('_', ' ').title()}"


def build_loop_collection(item_var: str) -> list:
    count = random.randint(3, 5)

    if any(x in item_var for x in ["order_item", "line_item", "item", "product"]):
        chars = string.ascii_uppercase + string.digits
        return [
            {
                item_var: get_mock_value("product_name"),
                "name": random.choice(PRODUCTS),
                "price": price(),
                "quantity": str(random.randint(1, 5)),
                "sku": f"SKU-{''.join(random.choices(chars, k=6))}",
                "url": url("order"),
            }
            for _ in range(count)
        ]

    if any(x in item_var for x in ["feature", "benefit", "highlight"]):
        features = [
            "Unlimited API calls", "Priority email support",
            "Advanced analytics dashboard", "Custom domain support",
            "Team collaboration tools", "SSO & SAML integration",
            "99.9% uptime SLA", "Dedicated account manager",
        ]
        return [
            {item_var: f} for f in random.sample(features, k=min(count, len(features)))
        ]

    if any(x in item_var for x in ["link", "nav_item", "menu_item"]):
        links = [
            {"label": "Dashboard", "url": url("dashboard")},
            {"label": "Settings",  "url": url("settings")},
            {"label": "Billing",   "url": url("billing")},
            {"label": "Help",      "url": url("help")},
        ]
        return [{item_var: lnk["label"], **lnk} for lnk in links[:count]]

    if any(x in item_var for x in ["member", "user", "teammate"]):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        return [
            {
                item_var: f"{first} {last}",
                "role": random.choice(ROLES),
                "email": email(first, last)
            }
            for _ in range(count)
        ]

    return [
        {item_var: get_mock_value(f"{item_var}_{i + 1}")} for i in range(count)
    ]
