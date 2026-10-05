"""OPTIONAL AI layer (not used by default). Needs: pip install anthropic; ANTHROPIC_API_KEY set.
Improves clause wording only; the deterministic template is always the fallback."""
import os


def refine_clause(text, model="claude-sonnet-5-5"):
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return text                      # no key -> use template text unchanged
    try:
        import anthropic
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model=model, max_tokens=300,
            system="Rewrite the clause in plain formal legal English. Do not add, "
                   "remove or change names, amounts, dates or obligations. Return only the clause.",
            messages=[{"role": "user", "content": text}])
        out = msg.content[0].text.strip()
        return out if out else text
    except Exception:
        return text                      # any failure -> safe fallback
