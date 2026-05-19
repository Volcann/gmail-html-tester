import random


def get_mock_value(var_name: str) -> str:
    name = var_name.lower()
    if any(x in name for x in ["first_name", "user", "name"]):
        return random.choice(["Alice", "Bob", "Charlie", "Diana", "Eve"])
    if any(x in name for x in ["url", "link", "href"]):
        return "https://example.com/link_" + str(random.randint(100, 999))
    if any(x in name for x in ["company", "org"]):
        return random.choice(["TechCorp", "GlobalNet", "Acme Corp"])
    if any(x in name for x in ["email", "mail"]):
        return f"user{random.randint(1000, 9999)}@example.com"
    if any(x in name for x in ["price", "cost", "amount", "total"]):
        return f"${random.randint(10, 150)}.99"
    if any(x in name for x in ["title", "subject", "header"]):
        return "Important Notification"
    if any(x in name for x in ["role"]):
        return random.choice(["Admin", "Editor", "Subscriber"])
    if any(x in name for x in ["date", "year"]):
        return str(2026)
    if any(x in name for x in ["code", "promo", "token"]):
        return f"SAVE{random.randint(10, 50)}"
    if any(x in name for x in ["desc", "message", "intro", "note", "tagline"]):
        return random.choice([
            "Welcome to our platform!",
            "Thank you for being with us.",
            "Action is required on your account."
        ])
    if any(x in name for x in ["badge", "status"]):
        return random.choice(["New", "Active", "Pending", "Premium"])
    return f"Sample {var_name.capitalize()}"


def build_mock_context(
    all_vars: set[str],
    if_flags: list[str],
    for_loops: list[tuple[str, str]]
) -> dict:
    ctx = {}
    for item_v, coll_v in for_loops:
        ctx[coll_v] = [
            {item_v: get_mock_value(item_v + "_1")},
            {item_v: get_mock_value(item_v + "_2")},
            {item_v: get_mock_value(item_v + "_3")}
        ]

    loops_v = {item for item, _ in for_loops}
    loops_c = {coll for _, coll in for_loops}
    skip = loops_c | loops_v | set(if_flags)
    remaining = sorted(all_vars - skip)

    for var in remaining:
        ctx[var] = get_mock_value(var)

    for flag in if_flags:
        ctx[flag] = True

    return ctx
