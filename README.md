# rule-precedence

Stacked rule layers (org, team, project) where a lower layer may tighten a rule but any attempt to loosen one is rejected and reported.

**This is a scripted demo.** It represents the governance process I use in Palladium, my own agent framework. It is not a sample or excerpt of that system, and no Palladium code or data is in it.

- Live page: https://demos.obviouslogic.ai/rule-precedence/
- Source: https://github.com/obviouslogic-ai/rule-precedence

## How it fits Palladium governance

Palladium stacks its rules, from a top-level charter down to each agent's task. Lower layers can add rules or make them stricter, never weaker. This repo acts that out with three rule types: flags, maximums and allow-lists.

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

The page fits one screen. Pick one proposed rule change at the bottom. The page checks it against every layer above it, then lights it applied or rejected and updates the effective rules. Press **Replay** or pick another. The explanation sits behind **About this demo** in the corner. Add `?fast=1` to skip the pauses.

The page runs this repo's real Python in the browser through Pyodide, so what you click is the same code the tests cover. Styling comes from `web/kit/`, shared across all five demos.

## Tests

```sh
python3 -m unittest -v
```

## License

MIT
