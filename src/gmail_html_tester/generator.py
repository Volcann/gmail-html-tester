import itertools

_MAX_VARIANTS = 64


def build_variants(base_ctx: dict, if_flags: list) -> list:
    if not if_flags:
        return [("all-conditions-off", base_ctx)]

    combos = list(itertools.product([True, False], repeat=len(if_flags)))
    if len(combos) > _MAX_VARIANTS:
        combos = combos[:_MAX_VARIANTS]

    variants = []
    for combo in combos:
        ctx = dict(base_ctx)
        on_flags = []
        off_flags = []

        for flag, value in zip(if_flags, combo):
            if value:
                ctx[flag] = base_ctx.get(flag, True)
                on_flags.append(flag)
            else:
                ctx[flag] = False
                off_flags.append(flag)

        parts = []
        if on_flags:
            parts.append("ON:" + "+".join(on_flags))
        if off_flags:
            parts.append("OFF:" + "+".join(off_flags))
        label = " | ".join(parts) if parts else "base"
        variants.append((label, ctx))

    return variants
