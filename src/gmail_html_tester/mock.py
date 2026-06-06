import random
import string
from datetime import datetime, timedelta

_FIRST_NAMES = [
    "James", "Sarah", "Michael", "Emily", "David", "Olivia",
    "Daniel", "Sophia", "Ethan", "Isabella", "Liam", "Ava",
    "Noah", "Mia", "Lucas", "Charlotte", "Mason", "Amelia",
]

_LAST_NAMES = [
    "Anderson", "Thompson", "Garcia", "Martinez", "Robinson",
    "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall",
    "Allen", "Young", "Hernandez", "King", "Wright", "Lopez",
]

_COMPANIES = [
    "Stripe", "Notion", "Linear", "Vercel", "Figma", "Supabase",
    "PlanetScale", "Railway", "Fly.io", "Cloudflare", "Resend",
    "Lemon Squeezy", "Paddle", "Render", "Netlify",
]

_SCHOOLS = [
    "Westlake Academy", "Riverdale High School", "Pinecrest Institute",
    "Summit Preparatory School", "Greenfield College",
    "Oakridge Learning Center", "Crestview Charter School",
    "Maplewood High School",
]

_DOMAINS = [
    "acmecorp.io", "getnotion.com", "linear.app", "vercel.app",
    "stripe.com", "supabase.io", "cloudflare.com", "figma.com",
]

_PRODUCTS = [
    "Pro Plan Subscription", "Enterprise License", "Starter Pack",
    "Annual Membership", "Lifetime Access", "Team Seat (x5)",
    "API Add-on", "Priority Support Bundle",
]

_CATEGORIES = [
    "Electronics", "Home & Garden", "Books & Media", "Clothing",
    "Sports & Outdoors", "Health & Beauty", "Toys & Games", "Office Supplies",
]

_PLAN_NAMES = [
    "Starter", "Growth", "Pro", "Business", "Enterprise", "Ultimate",
]

_CURRENCIES = ["$", "€", "£"]

_ROLES = [
    "Admin", "Manager", "Editor", "Viewer", "Owner", "Contributor", "Analyst"
]

_STATUSES = [
    "Active", "Pending", "Processing", "Completed", "On Hold", "Cancelled"
]

_BADGE_LABELS = ["New", "Verified", "Premium", "Beta", "Featured", "Trusted"]

_CTA_TEXTS = [
    "Get Started", "View Dashboard", "Confirm Account", "Download Invoice",
    "Track Your Order", "Activate Now", "Claim Offer", "Review Details",
]

_SUPPORT_EMAILS = [
    "support@acmecorp.io", "help@getnotion.com", "team@linear.app",
]

_CITIES = [
    "San Francisco, CA", "New York, NY", "Austin, TX", "Seattle, WA",
    "Boston, MA", "Chicago, IL", "Los Angeles, CA", "Denver, CO",
]

_BASE_URLS = [
    "https://app.acmecorp.io",
    "https://dashboard.getnotion.com",
    "https://linear.app",
    "https://vercel.app",
]


def _make_order_id() -> str:
    return f"ORD-{random.randint(100000, 999999)}"


def _make_invoice_id() -> str:
    return f"INV-{random.randint(2024100, 2024999)}"


def _make_ticket_id() -> str:
    return f"TKT-{random.randint(10000, 99999)}"


def _make_promo_code() -> str:
    return f"SAVE{random.randint(10, 50)}"


def _make_token() -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=32))


def _make_url(path_key: str = "dashboard") -> str:
    base = random.choice(_BASE_URLS)
    paths = {
        "login": "/auth/login",
        "signup": "/auth/register",
        "dashboard": "/dashboard",
        "settings": "/settings/profile",
        "billing": "/settings/billing",
        "upgrade": "/upgrade?ref=email",
        "confirm": f"/confirm?token={_make_token()}",
        "reset": f"/auth/reset-password?token={_make_token()}",
        "unsubscribe": f"/unsubscribe?uid={_make_token()[:16]}",
        "invoice": f"/invoices/{_make_invoice_id()}",
        "order": f"/orders/{_make_order_id()}",
        "track": f"/shipping/track?id={_make_order_id()}",
        "profile": "/profile/edit",
        "help": "/help",
        "privacy": "/legal/privacy",
        "terms": "/legal/terms",
    }
    path = paths.get(path_key, "/")
    return base + path


def _make_date(offset_days: int = 0, fmt: str = "%B %d, %Y") -> str:
    return (datetime.now() + timedelta(days=offset_days)).strftime(fmt)


def _make_email(first: str = "", last: str = "") -> str:
    domain = random.choice(_DOMAINS)
    if first and last:
        return f"{first.lower()}.{last.lower()}@{domain}"
    return f"user{random.randint(1000, 9999)}@{domain}"


def _make_price() -> str:
    currency = random.choice(_CURRENCIES)
    amount = random.choice([
        9.99, 19.99, 29.99, 49.99, 79.99, 99.99, 149.00, 299.00
    ])
    return f"{currency}{amount:,.2f}"


def get_mock_value(var_name: str) -> str:
    name = var_name.lower().replace(".", "_")

    if any(x in name for x in ["first_name", "firstname"]):
        return random.choice(_FIRST_NAMES)
    if any(x in name for x in ["last_name", "lastname", "surname"]):
        return random.choice(_LAST_NAMES)
    if any(x in name for x in ["full_name", "fullname"]):
        return f"{random.choice(_FIRST_NAMES)} {random.choice(_LAST_NAMES)}"
    if any(x in name for x in ["username", "user_name", "handle"]):
        return f"{random.choice(_FIRST_NAMES).lower()}{random.randint(10, 99)}"
    if any(x in name for x in ["student_name", "student"]):
        return f"{random.choice(_FIRST_NAMES)} {random.choice(_LAST_NAMES)}"
    if "name" in name:
        return f"{random.choice(_FIRST_NAMES)} {random.choice(_LAST_NAMES)}"

    if any(x in name for x in ["email", "mail_address", "mailaddress"]):
        return _make_email(
            random.choice(_FIRST_NAMES),
            random.choice(_LAST_NAMES),
        )
    if "support_email" in name:
        return random.choice(_SUPPORT_EMAILS)

    if any(x in name for x in ["unsubscribe_url", "unsubscribe_link"]):
        return _make_url("unsubscribe")
    if any(x in name for x in ["login_url", "signin_url", "sign_in_url"]):
        return _make_url("login")
    if any(x in name for x in ["signup_url", "register_url"]):
        return _make_url("signup")
    if any(x in name for x in ["dashboard_url", "dashboard_link"]):
        return _make_url("dashboard")
    if any(x in name for x in ["billing_url", "billing_link"]):
        return _make_url("billing")
    if any(x in name for x in ["upgrade_url", "upgrade_link"]):
        return _make_url("upgrade")
    if any(
        x in name for x in [
            "confirm_url", "confirmation_url", "verify_url", "verification_url"
        ]
    ):
        return _make_url("confirm")
    if any(x in name for x in ["reset_url", "reset_link", "password_reset"]):
        return _make_url("reset")
    if any(x in name for x in ["invoice_url", "invoice_link"]):
        return _make_url("invoice")
    if any(x in name for x in ["order_url", "order_link"]):
        return _make_url("order")
    if any(x in name for x in ["track_url", "tracking_url", "tracking_link"]):
        return _make_url("track")
    if any(x in name for x in ["profile_url", "profile_link"]):
        return _make_url("profile")
    if any(x in name for x in ["help_url", "help_link", "support_url"]):
        return _make_url("help")
    if any(x in name for x in ["privacy_url", "privacy_link"]):
        return _make_url("privacy")
    if any(x in name for x in ["terms_url", "terms_link"]):
        return _make_url("terms")
    if any(x in name for x in ["cta_url", "action_url", "button_url"]):
        return _make_url("dashboard")
    if any(x in name for x in ["url", "link", "href"]):
        return _make_url("dashboard")

    if any(
        x in name for x in [
            "company_name", "company", "org_name",
            "organisation", "organization"
        ]
    ):
        return random.choice(_COMPANIES)
    if "school" in name:
        return random.choice(_SCHOOLS)
    if "brand" in name:
        return random.choice(_COMPANIES)

    if any(
        x in name for x in [
            "price", "amount", "cost", "total", "subtotal",
            "tax", "fee", "charge", "balance", "refund",
            "discount_amount", "savings"
        ]
    ):
        return _make_price()
    if "plan_price" in name or "monthly_price" in name:
        return _make_price()
    if "annual_price" in name:
        return _make_price()

    if any(x in name for x in ["plan_name", "plan", "tier", "subscription"]):
        return random.choice(_PLAN_NAMES)
    if "billing_cycle" in name:
        return random.choice(["Monthly", "Annual"])
    if "seats" in name or "seat_count" in name:
        return str(random.randint(2, 25))

    if any(x in name for x in ["order_id", "order_number"]):
        return _make_order_id()
    if any(x in name for x in ["invoice_id", "invoice_number"]):
        return _make_invoice_id()
    if any(x in name for x in ["ticket_id", "ticket_number", "ticket"]):
        return _make_ticket_id()
    if any(
        x in name for x in ["promo_code", "coupon", "discount_code", "voucher"]
    ):
        return _make_promo_code()
    if any(
        x in name for x in ["token", "api_key", "secret", "verification_code"]
    ):
        return _make_token()
    if any(x in name for x in ["transaction_id", "payment_id"]):
        txn_part = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=12)
        )
        return f"TXN-{txn_part}"

    if any(
        x in name for x in [
            "renewal_date", "next_billing_date", "next_charge_date"
        ]
    ):
        return _make_date(offset_days=random.randint(1, 30))
    if any(
        x in name for x in [
            "expiry_date", "expiration_date", "expires_at", "expire_date"
        ]
    ):
        return _make_date(offset_days=random.randint(3, 14))
    if any(x in name for x in ["due_date", "payment_due"]):
        return _make_date(offset_days=random.randint(7, 30))
    if any(
        x in name for x in ["date", "created_at", "updated_at", "timestamp"]
    ):
        return _make_date()
    if "year" in name:
        return str(datetime.now().year)
    if "time" in name:
        return datetime.now().strftime("%I:%M %p")

    if any(x in name for x in ["address", "city", "location"]):
        return random.choice(_CITIES)
    if "country" in name:
        return random.choice(
            ["United States", "United Kingdom", "Canada", "Australia"]
        )
    if "postal_code" in name or "zip_code" in name or "zipcode" in name:
        return f"{random.randint(10000, 99999)}"

    if any(x in name for x in ["role", "permission", "access_level"]):
        return random.choice(_ROLES)
    if "department" in name:
        return random.choice(
            ["Engineering", "Marketing", "Sales", "Support", "Design"]
        )

    if any(
        x in name for x in [
            "status",
            "state",
            "order_status",
            "payment_status",
        ]
    ):
        return random.choice(_STATUSES)
    if any(x in name for x in ["badge", "badge_label", "label"]):
        return random.choice(_BADGE_LABELS)

    if any(x in name for x in ["product_name", "item_name", "product"]):
        return random.choice(_PRODUCTS)
    if "category" in name:
        return random.choice(_CATEGORIES)
    if "quantity" in name or "qty" in name:
        return str(random.randint(1, 10))
    if "sku" in name:
        sku_part = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=8)
        )
        return f"SKU-{sku_part}"

    if any(
        x in name for x in [
            "cta_text", "button_text", "button_label", "action_label"
        ]
    ):
        return random.choice(_CTA_TEXTS)

    if any(x in name for x in ["subject", "email_subject"]):
        return random.choice([
            "Your order is confirmed",
            "Welcome aboard — let's get started",
            "Action required on your account",
            "Your invoice is ready",
            "Password reset request",
        ])
    if any(x in name for x in ["title", "heading", "headline"]):
        return random.choice([
            "Welcome to the Platform",
            "Your Account Has Been Created",
            "Action Required",
            "Order Confirmed",
            "Invoice Ready",
        ])
    if any(
        x in name for x in [
            "message", "body", "content", "intro", "description", "desc"
        ]
    ):
        return random.choice([
            "We're excited to have you on board. Everything is set up.",
            "A quick heads-up about your account — please review the details.",
            "Your request has been processed successfully.",
            "Thank you for your continued trust. We're here if you need help.",
        ])
    if any(x in name for x in ["tagline", "subtitle", "subheading"]):
        return random.choice([
            "The fastest way to get things done.",
            "Simple, powerful, and built for teams.",
            "Everything you need, nothing you don't.",
        ])
    if any(x in name for x in ["note", "footnote", "footer_note"]):
        return "This is an automated message. Please do not reply."
    if any(x in name for x in ["greeting", "salutation"]):
        return f"Hello, {random.choice(_FIRST_NAMES)}!"
    if any(x in name for x in ["signature", "sign_off"]):
        return f"The {random.choice(_COMPANIES)} Team"

    if any(x in name for x in ["count", "total_count", "num", "number"]):
        return str(random.randint(1, 50))
    if any(x in name for x in ["percentage", "percent", "rate"]):
        return f"{random.randint(5, 40)}%"
    if any(x in name for x in ["days_left", "days_remaining", "days_until"]):
        return str(random.randint(1, 30))

    if any(x in name for x in ["phone", "phone_number", "mobile"]):
        return (
            f"+1 ({random.randint(200, 999)}) "
            f"{random.randint(200, 999)}-{random.randint(1000, 9999)}"
        )

    return f"Sample {var_name.replace('_', ' ').title()}"


def build_mock_context(
    all_vars: set,
    if_flags: list,
    for_loops: list,
) -> dict:
    ctx = {}

    for item_var, collection_var in for_loops:
        ctx[collection_var] = _build_loop_collection(item_var)

    loop_items = {item for item, _ in for_loops}
    loop_colls = {coll for _, coll in for_loops}
    skip = loop_colls | loop_items | set(if_flags)
    remaining = sorted(all_vars - skip)

    for var in remaining:
        ctx[var] = get_mock_value(var)

    for flag in if_flags:
        ctx[flag] = True

    return ctx


def _build_loop_collection(item_var: str) -> list:
    count = random.randint(3, 5)

    if any(
        x in item_var for x in ["order_item", "line_item", "item", "product"]
    ):
        sku_part = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        return [
            {
                item_var: get_mock_value("product_name"),
                "name": random.choice(_PRODUCTS),
                "price": _make_price(),
                "quantity": str(random.randint(1, 5)),
                "sku": f"SKU-{sku_part}",
                "url": _make_url("order"),
            }
            for _ in range(count)
        ]

    if any(x in item_var for x in ["feature", "benefit", "highlight"]):
        features = [
            "Unlimited API calls",
            "Priority email support",
            "Advanced analytics dashboard",
            "Custom domain support",
            "Team collaboration tools",
            "SSO & SAML integration",
            "99.9% uptime SLA",
            "Dedicated account manager",
        ]
        sampled = random.sample(features, k=min(count, len(features)))
        return [{item_var: f} for f in sampled]

    if any(x in item_var for x in ["link", "nav_item", "menu_item"]):
        links = [
            {"label": "Dashboard", "url": _make_url("dashboard")},
            {"label": "Settings", "url": _make_url("settings")},
            {"label": "Billing", "url": _make_url("billing")},
            {"label": "Help", "url": _make_url("help")},
        ]
        return [{item_var: lnk["label"], **lnk} for lnk in links[:count]]

    if any(x in item_var for x in ["member", "user", "teammate"]):
        first = random.choice(_FIRST_NAMES)
        last = random.choice(_LAST_NAMES)
        return [
            {
                item_var: f"{first} {last}",
                "role": random.choice(_ROLES),
                "email": _make_email(first, last),
            }
            for _ in range(count)
        ]

    return [
        {item_var: get_mock_value(f"{item_var}_{i + 1}")}
        for i in range(count)
    ]
