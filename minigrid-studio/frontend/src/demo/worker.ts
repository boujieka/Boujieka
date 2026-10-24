/// <reference lib="webworker" />
// Runs the Python engine (the same code as the server) in Pyodide, off the main thread.
// Messages: { id, fn, args } -> { id, ok, value | error }.

interface PyFn { (...a: unknown[]): string }
let ready: Promise<Record<string, PyFn>> | null = null;

async function boot(base: string): Promise<Record<string, PyFn>> {
  const url = `${base}pyodide/pyodide.mjs`;
  const { loadPyodide } = await import(/* @vite-ignore */ url);
  const py = await loadPyodide({ indexURL: `${base}pyodide/` });
  const zip = await (await fetch(`${base}py/mgs.zip`)).arrayBuffer();
  py.unpackArchive(zip, "zip", { extractDir: "/home/pyodide/mgs" });
  py.runPython("import sys; sys.path.insert(0, '/home/pyodide/mgs')");
  const mod = py.pyimport("app.demo.browser");
  const names = ["meta", "revise", "run", "compare", "studio_xlsx"];
  return Object.fromEntries(names.map((n) => [n, (...a: unknown[]) => mod[n](...a) as string]));
}

self.onmessage = async (e: MessageEvent<{ id: number; fn: string; args: unknown[]; base: string }>) => {
  const { id, fn, args, base } = e.data;
  try {
    ready ??= boot(base);
    const fns = await ready;
    const value = fns[fn](...args);
    (self as unknown as Worker).postMessage({ id, ok: true, value });
  } catch (err) {
    (self as unknown as Worker).postMessage({ id, ok: false, error: String(err) });
  }
};
