// Shared header, nav, sample note, telemetry clock and scroll reveal for the governance demos.
export const DEMOS = [
  ["human-approval-gate", "Approval gate"], ["rule-precedence", "Rule precedence"], ["skill-registry-lint", "Skill lint"],
  ["agent-activity-viz", "Agent activity"], ["assembly-demo", "Assembly"]];
export const NOTE = "This is a scripted demo. It represents the governance process I use in Palladium, my own agent framework. It is not a sample or excerpt of that system, and no Palladium code or data is in it.";
const LIVE = location.hostname === "demos.obviouslogic.ai";
export const href = n => LIVE ? `/${n}/` : `/${n}/web/`;
export function mount(current, { status = "READY" } = {}) {
  const i = DEMOS.findIndex(d => d[0] === current);
  const h = document.createElement("header"); h.className = "kit-head";
  h.innerHTML = `<a class="brand" href="${LIVE ? "/" : "/demos-site/"}">ObviousLogic / Demos</a>
    <nav>${DEMOS.map(([n, t], j) => `<a href="${href(n)}"${j === i ? ' aria-current="page"' : ""}><span class="n">${String(j + 1).padStart(2, "0")}</span><span class="t"> ${t}</span></a>`).join("")}</nav>
    <span class="clock" id="kit-clock"></span>`;
  document.body.prepend(h);
  document.querySelectorAll("[data-kit-note]").forEach(n => { n.classList.add("note"); n.textContent = NOTE; });
  document.querySelectorAll("[data-kit-tele]").forEach(n => n.innerHTML = `DEMO ${String(i + 1).padStart(2, "0")} / <b>${(DEMOS[i] || ["", ""])[1].toUpperCase()}</b> &nbsp; STATUS <b id="kit-status">${status}</b>`);
  const f = document.createElement("footer"); f.className = "kit-foot tele";
  const src = i >= 0 ? `SOURCE <a href="https://github.com/obviouslogic-ai/${current}">github<span class="long">.com/obviouslogic-ai/${current}</span></a>` : "";
  if (document.body.classList.contains("stage")) {
    f.innerHTML = `<span>SCRIPTED DEMO<span class="long"> OF PALLADIUM GOVERNANCE</span></span><span>${src}</span><button class="info-btn" id="kit-info-btn" aria-expanded="false">i  ABOUT THIS DEMO</button>`;
    const box = document.createElement("aside"); box.className = "kit-info"; box.id = "kit-info";
    const t = document.getElementById("info");
    box.innerHTML = `<div class="tele">ABOUT</div>${t ? t.innerHTML : ""}<p class="note">${NOTE}</p>`;
    document.body.append(f, box);
    const b = document.getElementById("kit-info-btn");
    b.onclick = () => b.setAttribute("aria-expanded", box.classList.toggle("open"));
  } else {
    if (i >= 0) f.innerHTML = `${src} &nbsp; / &nbsp; PAGE demos.obviouslogic.ai/${current} &nbsp; / &nbsp; <a href="https://obviouslogic.ai">obviouslogic.ai</a>`;
    document.body.append(f);
  }
  const tick = () => { const c = document.getElementById("kit-clock"); if (c) c.textContent = new Date().toISOString().slice(11, 19) + " UTC"; };
  tick(); setInterval(tick, 1000);
  const io = new IntersectionObserver(es => es.forEach(e => e.isIntersecting && e.target.classList.add("in")), { threshold: .1 });
  document.querySelectorAll(".screen").forEach(s => io.observe(s));
}
export const setStatus = s => { const n = document.getElementById("kit-status"); if (n) n.textContent = s; };
export const revealAll = () => document.querySelectorAll(".screen").forEach(s => s.classList.add("in"));
export const sleep = (ms, fast = new URLSearchParams(location.search).has("fast")) => new Promise(r => setTimeout(r, fast ? Math.min(ms, 40) : ms));

// Shrink the work area's type (--k, 1 down to .55) until the stage fits the screen with nothing clipped.
// Elements marked data-fit count as clipped when their content overflows them.
export function autoFit({ watch = true } = {}) {
  const main = document.querySelector(".stage-main"), b = document.body; if (!main) return () => {};
  const over = () => main.scrollHeight > main.clientHeight + 1 || main.scrollWidth > main.clientWidth + 1 ||
    [...main.querySelectorAll(".work,.work>:not([data-nofit]),[data-fit]")].some(e => e.scrollHeight > e.clientHeight + 1 || e.scrollWidth > e.clientWidth + 1);
  let queued = false;
  const run = () => { queued = false; let k = 1; b.style.setProperty("--k", k); while (over() && k > .49) { k = Math.round((k - .05) * 100) / 100; b.style.setProperty("--k", k); } };
  const fit = () => { if (!queued) { queued = true; requestAnimationFrame(run); } };
  addEventListener("resize", fit); addEventListener("transitionend", fit); addEventListener("animationend", fit); if (watch) { new MutationObserver(fit).observe(main, { childList: true, subtree: true, characterData: true }); new MutationObserver(fit).observe(b, { attributes: true, attributeFilter: ["data-done"] }); }
  run(); return run;
}
