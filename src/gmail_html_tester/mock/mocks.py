import json

from google import genai

from gmail_html_tester.config import settings

from .utils import build_loop_collection, get_mock_value


def build_mock_context(all_vars: set, if_flags: list, for_loops: list) -> dict:
    ctx = {}

    for item_var, collection_var in for_loops:
        ctx[collection_var] = build_loop_collection(item_var)

    loop_items = {item for item, _ in for_loops}
    loop_colls = {coll for _, coll in for_loops}
    skip = loop_colls | loop_items | set(if_flags)

    for var in sorted(all_vars - skip):
        ctx[var] = get_mock_value(var)

    for flag in if_flags:
        ctx[flag] = True

    return ctx


def build_ai_mocks(
    variables: list[str],
    api_key: str | None = None,
) -> dict[str, str]:
    key = api_key or settings.gemini_api_key
    if not key:
        return {v: get_mock_value(v) for v in variables}

    prompt = (
        f"Generate realistic mock values for these email template variables: "
        f"{', '.join(variables)}. "
        "Return ONLY a flat JSON object where each key is a variable name "
        "and each value is a realistic string. No explanation, no markdown."
    )

    try:
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        text = (
            response.text.strip()
            .removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )
        result = json.loads(text)

        for v in variables:
            if v not in result:
                result[v] = get_mock_value(v)

        return result

    except Exception as e:
        print(f"  ⚠  Gemini error: {e}. Using local mocks.")
        return {v: get_mock_value(v) for v in variables}
