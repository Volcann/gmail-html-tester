import itertools


def build_variants(base_ctx: dict, if_flags: list[str]) -> list[tuple[str, dict]]:
    if not if_flags:
        return [("(no conditions)", base_ctx)]

    combos = list(itertools.product([True, False], repeat=len(if_flags)))
    if len(combos) > 64:
        combos = combos[:64]

    variants = []
    for combo in combos:
        label_parts = []
        ctx = dict(base_ctx)
        for flag, value in zip(if_flags, combo):
            if value:
                ctx[flag] = base_ctx.get(flag, "yes")
                label_parts.append(f"{flag}=T")
            else:
                ctx[flag] = ""
                label_parts.append(f"{flag}=F")
        variants.append((", ".join(label_parts), ctx))

    return variants
