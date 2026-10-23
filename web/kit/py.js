// Load Pyodide from ./vendor and copy the repo's real Python files into its filesystem.
export async function loadPy(files) {
  const py = await globalThis.loadPyodide({ indexURL: new URL("../vendor/", import.meta.url).href });
  for (const [name, url] of Object.entries(files)) {
    const path = "/home/pyodide/" + name; const dir = path.slice(0, path.lastIndexOf("/"));
    py.FS.mkdirTree(dir); py.FS.writeFile(path, await (await fetch(url)).text());
  }
  py.runPython('import sys; sys.path.insert(0, "/home/pyodide")');
  return py;
}
