"""Input validation and sanitisation for LegalEase."""
import re
from xml.sax.saxutils import escape

DEFAULTS = {
    "name": "Sample User",
    "other_party": "Sample Party",
    "purpose": "General legal arrangement",
    "duration": "12 months",
    "amount": "10000",
    "deposit": "0",
    "notice": "30 days",
    "place": "India",
}
MAX_LEN = 200
VALID_TYPES = {"rental", "nda", "employment", "leave"}


def clean_text(value, default):
    """Strip whitespace, apply default for blank values, limit length."""
    value = (value or "").strip()
    return (value or default)[:MAX_LEN]


def clean_amount(value, default):
    """Return amount as digits with thousand separators, or raise ValueError."""
    raw = (value or "").replace(",", "").strip() or default
    if not re.fullmatch(r"\d{1,9}(\.\d{1,2})?", raw):
        raise ValueError("Amount must be a positive number (max 9 digits).")
    num = float(raw)
    return f"{num:,.0f}" if num.is_integer() else f"{num:,.2f}"


def validate(form):
    """Validate a form dict. Returns (data, errors)."""
    errors, data = [], {}
    doc_type = form.get("document_type", "rental")
    if doc_type not in VALID_TYPES:
        errors.append("Unknown document type.")
    data["document_type"] = doc_type
    for key in ("name", "other_party", "purpose", "duration", "notice", "place"):
        data[key] = clean_text(form.get(key), DEFAULTS[key])
    for key in ("amount", "deposit"):
        try:
            data[key] = clean_amount(form.get(key), DEFAULTS[key])
        except ValueError as exc:
            errors.append(f"{key.title()}: {exc}")
            data[key] = DEFAULTS[key]
    if data["name"].lower() == data["other_party"].lower():
        errors.append("The two parties must have different names.")
    return data, errors


def safe(text):
    """Escape text for ReportLab Paragraph markup."""
    return escape(text)
