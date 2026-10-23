#!/bin/sh
# Download the pinned Pyodide core into web/vendor (not committed; about 14 MB).
set -e; cd "$(dirname "$0")"; V=0.27.7; T=$(mktemp -d)
(cd "$T" && npm pack "pyodide@$V" -q >/dev/null && tar xzf "pyodide-$V.tgz")
mkdir -p vendor && for f in pyodide.js pyodide.mjs pyodide.asm.js pyodide.asm.wasm python_stdlib.zip pyodide-lock.json; do cp "$T/package/$f" vendor/; done
echo "Pyodide $V in web/vendor"
