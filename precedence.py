"""Rule precedence: layered policy where lower layers may add or tighten, never weaken.

Layers are applied in order, for example org -> team -> project. Each rule is one of:
  {"type": "flag", "value": bool}     True is stricter (e.g. require_review)
  {"type": "max", "value": number}    lower is stricter (e.g. max_spend)
  {"type": "allow", "value": [..]}    smaller set is stricter (e.g. allowed_tools)
"""
import json
import sys
from pathlib import Path


class Weakening(Exception):
    pass


def stricter_or_equal(kind, new, old):
    if kind == "flag":
        return new or not old
    if kind == "max":
        return new <= old
    if kind == "allow":
        return set(new) <= set(old)
    raise ValueError(f"unknown rule type: {kind}")


def merge(layers):
    """Return (effective rules, violations). Weakening attempts are rejected, not applied."""
    effective, violations = {}, []
    for layer in layers:
        for name, rule in layer["rules"].items():
            current = effective.get(name)
            if current is None:
                effective[name] = dict(rule, set_by=layer["name"])
                continue
            if rule["type"] != current["type"]:
                violations.append(f"{layer['name']}: {name} changes type")
            elif not stricter_or_equal(rule["type"], rule["value"], current["value"]):
                violations.append(
                    f"{layer['name']}: {name} tries to weaken {current['value']!r} "
                    f"(set by {current['set_by']}) to {rule['value']!r}"
                )
            else:
                effective[name] = dict(rule, set_by=layer["name"])
    return effective, violations


def check(layers):
    effective, violations = merge(layers)
    if violations:
        raise Weakening("; ".join(violations))
    return effective


if __name__ == "__main__":
    layers = json.loads(Path(sys.argv[1] if len(sys.argv) > 1 else "example.json").read_text())
    effective, violations = merge(layers)
    for name, rule in effective.items():
        print(f"{name:16} = {rule['value']!r:24} (set by {rule['set_by']})")
    for v in violations:
        print("REJECTED", v)
    sys.exit(1 if violations else 0)
