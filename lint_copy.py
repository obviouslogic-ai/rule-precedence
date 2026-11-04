#!/usr/bin/env python3
"""Fail if user-facing copy leaves the verified rule-precedence wording.

Scans the README, the page, and the shared demo kit. Prose is checked for
digits and for numbers spelled as words. The license is checked for forbidden
claims only: the copyright line keeps its legal name, and this script does
not edit or name-check legal text. The rule engine, fixtures, and tests are
out of scope.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

LAYERS = (
    "Charter",
    "Agent code",
    "Operator (build work only)",
    "Department",
    "Client adjustment",
)
LEAD = "A lower layer can add or tighten a rule and can never weaken one."
SENTENCE = "When a higher layer overrides a lower one, the override is recorded."
RATIFY = "A weakening draft is refused when it is ratified."

SPELLED_NUMBERS = (
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
    "thirteen",
    "fourteen",
    "fifteen",
    "sixteen",
    "seventeen",
    "eighteen",
    "nineteen",
    "twenty",
    "hundred",
    "thousand",
)


def _claim_patterns():
    return (
        re.compile("every" + r"\s+" + "attempt", re.I),
        re.compile("every" + r"\s+" + "single" + r"\s+" + "attempt", re.I),
        re.compile("any" + r"\s+" + "attempt", re.I),
        re.compile(r"\b" + "reported" + r"\b", re.I),
        re.compile("hash" + r"[-\s]?" + "chain", re.I),
        re.compile("tamper" + r"[-\s]?" + "proof", re.I),
        re.compile("tamper" + r"[-\s]?" + "evident", re.I),
        re.compile("immutab", re.I),
        re.compile("write" + r"[-\s]" + "once", re.I),
        re.compile("cannot" + r"\s+be\s+" + "altered", re.I),
        re.compile(r"\$\s*\d"),
        re.compile(r"\b" + "savings" + r"\b", re.I),
        re.compile(r"\b" + "overspend" + r"\b", re.I),
    )


def _person_names():
    return ("dan", "de" + "zago")


def _layer_and_role_phrases():
    return (
        "Operator (build work only)",
        "Agent code",
        "Client adjustment",
        "Charter",
        "Operator",
        "Department",
        "agent",
        "operator",
        "department",
        "charter",
        "client",
    )


def check_claims(text):
    errors = []
    for pattern in _claim_patterns():
        match = pattern.search(text)
        if match:
            errors.append(f"forbidden claim: {match.group(0)}")
    return errors


def check_names(text):
    """Match a person-name list, including a single name and any letter case.

    Layer and role words are removed first so they cannot match a name token.
    """
    held = text
    for phrase in _layer_and_role_phrases():
        held = re.sub(re.escape(phrase), " ", held, flags=re.I)
    errors = []
    for name in _person_names():
        match = re.search(r"\b" + re.escape(name) + r"\b", held, re.I)
        if match:
            errors.append(f"real-person name: {match.group(0)}")
    return errors


def check_digits(text):
    match = re.search(r"\d", text)
    if match:
        return [f"number in copy near: {text[max(0, match.start() - 24):match.end() + 24]!r}"]
    return []


def check_spelled_numbers(text):
    errors = []
    for word in SPELLED_NUMBERS:
        match = re.search(r"\b" + word + r"\b", text, re.I)
        if match:
            errors.append(f"spelled number: {match.group(0)}")
    return errors


def without_canon(text):
    for line in (LEAD, SENTENCE):
        text = text.replace(line, " ")
    return text


def require_story(text):
    errors = []
    lead_at = text.find(LEAD)
    sent_at = text.find(SENTENCE)
    if lead_at < 0:
        errors.append("missing the lead line")
    if sent_at < 0:
        errors.append("missing the override sentence")
    if lead_at >= 0 and sent_at >= 0 and lead_at > sent_at:
        errors.append("override sentence must follow the lead line")
    if RATIFY not in text:
        errors.append("missing the ratification line")
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


def _scan(label, text, *, digits=False, spelled=False, names=True):
    errors = []
    for error in check_claims(text):
        errors.append(f"{label}: {error}")
    if names:
        for error in check_names(text):
            errors.append(f"{label}: {error}")
    if digits:
        for error in check_digits(text):
            errors.append(f"{label}: {error}")
    if spelled:
        for error in check_spelled_numbers(without_canon(text)):
            errors.append(f"{label}: {error}")
    return errors


def check_repo():
    errors = []
    readme = (ROOT / "README.md").read_text()
    prose = markdown_prose(readme)
    fences = "\n".join(re.findall(r"```.*?```", readme, flags=re.S))
    errors.extend(_scan("README prose", prose, digits=True, spelled=True))
    errors.extend(_scan("README code", fences, digits=False, spelled=False))
    for error in require_story(prose):
        errors.append(f"README prose: {error}")

    page = (ROOT / "web" / "index.html").read_text()
    page_prose, page_code = html_parts(page)
    errors.extend(_scan("page prose", page_prose, digits=True, spelled=True))
    errors.extend(_scan("page code", page_code, digits=False, spelled=False))
    for error in require_story(page_prose):
        errors.append(f"page prose: {error}")

    kit = (ROOT / "web" / "kit" / "kit.js").read_text()
    errors.extend(_scan("kit", kit, digits=False, spelled=False))

    license_text = (ROOT / "LICENSE").read_text()
    errors.extend(_scan("LICENSE", license_text, digits=False, spelled=False, names=False))
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
