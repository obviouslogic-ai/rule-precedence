#!/usr/bin/env python3
"""Fail if user-facing copy leaves the verified rule-precedence wording.

Scans the README, the page, the shared demo note, and the license for
claims this demo must not make. Prose is also checked for digits. The
rule engine, fixtures, and tests are out of scope: their numbers are
behavior, not copy.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LAYERS = (
    "Charter",
    "Agent code",
    "Operator",
    "Department",
    "Client adjustment",
)
SENTENCE = "When a higher layer overrides a lower one, the override is recorded."

# Phrases are built here so the banned wording is not stored as a single literal.
def _claim_patterns():
    return (
        re.compile("every" + r"\s+" + "attempt", re.I),
        re.compile("any" + r"\s+" + "attempt", re.I),
        re.compile(r"\b" + "reported" + r"\b", re.I),
        re.compile("hash" + r"[-\s]?" + "chain", re.I),
        re.compile("tamper" + r"[-\s]?" + "proof", re.I),
        re.compile("tamper" + r"[-\s]?" + "evident", re.I),
        re.compile("immutab", re.I),
        re.compile(r"\$\s*\d"),
        re.compile(r"\b" + "savings" + r"\b", re.I),
        re.compile(r"\b" + "overspend" + r"\b", re.I),
    )


def _name_patterns():
    given = "Dan"
    family = "De" + "Zago"
    return (
        re.compile(r"\b" + given + r"\b"),
        re.compile(r"\b" + family + r"\b", re.I),
        re.compile(r"\b[A-Z][a-z]+ [A-Z][a-zA-Z]+\b"),
    )


def check_claims(text):
    errors = []
    for pattern in _claim_patterns():
        match = pattern.search(text)
        if match:
            errors.append(f"forbidden claim: {match.group(0)}")
    return errors


def check_names(text):
    errors = []
    for pattern in _name_patterns():
        match = pattern.search(text)
        if match:
            errors.append(f"real-person name: {match.group(0)}")
    return errors


def check_digits(text):
    match = re.search(r"\d", text)
    if match:
        return [f"number in copy near: {text[max(0, match.start() - 24):match.end() + 24]!r}"]
    return []


def require_story(text):
    errors = []
    if SENTENCE not in text:
        errors.append("missing the override sentence")
    indexes = []
    for layer in LAYERS:
        found = text.find(layer)
        if found < 0:
            errors.append(f"missing layer: {layer}")
            return errors
        indexes.append(found)
    if indexes != sorted(indexes):
        errors.append("layers are not in precedence order")
    return errors


def markdown_prose(text):
    return re.sub(r"```.*?```", " ", text, flags=re.S)


def html_parts(text):
    scripts = "\n".join(re.findall(r"<script\b[^>]*>.*?</script>", text, flags=re.I | re.S))
    styles = "\n".join(re.findall(r"<style\b[^>]*>.*?</style>", text, flags=re.I | re.S))
    prose = re.sub(r"<script\b[^>]*>.*?</script>", " ", text, flags=re.I | re.S)
    prose = re.sub(r"<style\b[^>]*>.*?</style>", " ", prose, flags=re.I | re.S)
    prose = re.sub(r"<[^>]+>", " ", prose)
    prose = prose.replace("&nbsp;", " ").replace("&amp;", "&")
    return prose, scripts + "\n" + styles


def check_repo():
    errors = []
    readme = (ROOT / "README.md").read_text()
    prose = markdown_prose(readme)
    fences = "\n".join(re.findall(r"```.*?```", readme, flags=re.S))
    for label, text, digits in (
        ("README prose", prose, True),
        ("README code", fences, False),
    ):
        for error in check_claims(text) + check_names(text) + (check_digits(text) if digits else []):
            errors.append(f"{label}: {error}")
    for error in require_story(prose):
        errors.append(f"README prose: {error}")

    page = (ROOT / "web" / "index.html").read_text()
    page_prose, page_code = html_parts(page)
    for error in check_claims(page_prose) + check_names(page_prose) + check_digits(page_prose):
        errors.append(f"page prose: {error}")
    for error in check_claims(page_code) + check_names(page_code):
        errors.append(f"page code: {error}")
    for error in require_story(page_prose):
        errors.append(f"page prose: {error}")

    kit = (ROOT / "web" / "kit" / "kit.js").read_text()
    for error in check_claims(kit) + check_names(kit):
        errors.append(f"kit: {error}")

    license_text = (ROOT / "LICENSE").read_text()
    for error in check_claims(license_text) + check_names(license_text):
        errors.append(f"LICENSE: {error}")
    return errors


def main():
    errors = check_repo()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("copy ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
