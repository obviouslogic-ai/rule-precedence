# Rule precedence

A lower layer can add or tighten a rule and can never weaken one.

When a higher layer overrides a lower one, the override is recorded.

A weakening draft is refused when it is ratified.

The precedence layers, in order, are Charter, Agent code, Operator (build work only), Department, and Client adjustment.

**This is a scripted demo that represents the process** I run in my own agent framework. It is not a sample or excerpt of that system, and none of its code or data is in it.

- Live page: https://demos.obviouslogic.ai/rule-precedence/
- Source: https://github.com/obviouslogic-ai/rule-precedence

## What this shows

Agent rules come from those layers. Ordinary merging lets the last file win, so a lower layer can lift a limit or switch review off. Precedence keeps the higher layer. The override is recorded.

The sample file uses short layer names to exercise that rule. It does not replace the order above.

The page and the command line run this repo. The last-write-wins path and the precedence path are both here.

## Run the CLI

```sh
python3 precedence.py example.json
```

Standard library only, no installs. The command prints the effective rules and the rejected weakenings.

## Run the page locally

```sh
cd web && ./get-pyodide.sh && cd ..
python3 -m http.server
```

Serve from this repo, then open the web page. The page fits the screen. Pick the example as written or a proposed change, then press **Merge the layers**. The table walks each rule. Each layer value is tagged tighter, looser, or set. Last write wins and precedence sit side by side. Rejected weakenings are listed. The explanation sits behind **About this demo**. Add a fast parameter to the page address to skip the pauses.

The page runs this repo's Python in the browser, so a click runs the same code the tests cover. Styling comes from `web/kit/`, shared with the other demos.

## Tests

```sh
python3 -m unittest -v
python3 lint_copy.py
```

## License

MIT
