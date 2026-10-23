# rule-precedence

A small demo of layered policy for AI agents. Rules flow down from the top layer (say, organization, then team, then project). A lower layer may add new rules or make existing ones stricter. It may never loosen a rule set above it.

## Rule types

| type  | stricter means          | example          |
|-------|-------------------------|------------------|
| flag  | `true` beats `false`    | `require_review` |
| max   | a lower number          | `max_spend`      |
| allow | a smaller set           | `allowed_tools`  |

A weakening attempt is rejected and reported, and the stricter value stays in force.

## Run it

```
python3 precedence.py example.json
```

The example's project layer tries to turn off review, and to raise the spend limit. Both are rejected. Its narrower tool list is accepted.

## Test it

```
python3 -m unittest -v
```

Python 3.10+, standard library only.

## Demo

Terminal recording: `demo.cast` (play with `asciinema play demo.cast`).
