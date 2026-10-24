# rule-precedence

Stacked rule layers (org, team, project) where a lower layer may tighten a rule but any attempt to loosen one is rejected and reported.

**This is a scripted demo that represents the process** I run in my own agent framework. It is not a sample or excerpt of that system, and none of its code or data is in it.

- Live page: https://demos.obviouslogic.ai/rule-precedence/
- Source: https://github.com/obviouslogic-ai/rule-precedence

## Why I built this

Agent rules come from several places: company policy, a team, one project. Ordinary config merging lets the last file win, so a single project setting can quietly lift a spend cap or switch off review for every run under it. My own framework stacks its rules from a top-level charter down to each task. Lower layers can add rules or make them stricter, never weaker, and every attempt to loosen one is reported. This repo acts that out with three rule types: flags, maximums and allow-lists.

## The cost, last write wins versus precedence

The page merges the same layers two ways, `naive()` (last write wins) and `effective()` (precedence), and prices the difference with an illustrative model. Every number is an input you can change; none are measured or cited figures.

- Overspend: runs a month x share of runs that spend to the cap x (loosened cap - policy cap).
- Review switched off: runs x share of unreviewed runs that go wrong x cost of one bad run.
- Defaults: 100 runs, 10% to the cap, 2% bad, $1,000 a bad run. On `example.json` that is $11,000 a month with last write wins and $0 with precedence.

## Run the CLI

```sh
python3 precedence.py example.json   # prints the effective rules and the rejected weakenings
```

Standard library only, no installs.

## Run the page locally

```sh
cd web && ./get-pyodide.sh && cd ..   # once: downloads Pyodide 0.27.7 into web/vendor (gitignored)
python3 -m http.server 8000   # from the folder that holds this repo
# open http://localhost:8000/rule-precedence/web/
```

The page fits one screen. Pick the example as written or one of four proposed changes, then press **Merge the layers**. The table walks rule by rule: each layer's value is tagged tighter, looser or set by `stricter_or_equal()`, then the last-write-wins result and the precedence result sit side by side with differences in red. Rejected weakenings are listed and the cost panel updates. The explanation sits behind **About this demo** in the corner. Add `?fast=1` to skip the pauses.

The page runs this repo's real Python in the browser through Pyodide, so what you click is the same code the tests cover. Styling comes from `web/kit/`, shared across all five demos.

## Tests

```sh
python3 -m unittest -v
```

## License

MIT
