// Shared header, nav, sample note, telemetry clock and scroll reveal for the governance demos.
export const DEMOS = [
  ["human-approval-gate", "Approval gate"], ["rule-precedence", "Rule precedence"], ["skill-registry-lint", "Skill lint"],
  ["agent-activity-viz", "Agent activity"], ["council-demo", "Council"]];
export const NOTE = "This is a scripted demo. It represents the governance process I use in Palladium, my own agent framework. It is not a sample or excerpt of that system, and no Palladium code or data is in it.";
const LIVE = location.hostname === "demos.obviouslogic.ai";
export const href = n => LIVE ? `/${n}/` : `/${n}/web/`;
export function mount(current, { status = "READY" } = {}) {
  const i = DEMOS.findIndex(d => d[0] === current);
  const h = document.createElement("header"); h.className = "kit-head";
  h.innerHTML = `<a class="brand" href="${LIVE ? "/" : "/demos-site/"}">ObviousLogic / Demos</a>
    <nav>${DEMOS.map(([n, t], j) => `<a href="${href(n)}"${j === i ? ' aria-current="page"' : ""}>${String(j + 1).padStart(2, "0")} ${t}</a>`).join("")}</nav>
    <span class="clock" id="kit-clock"></span>`;
  document.body.prepend(h);
  document.querySelectorAll("[data-kit-note]").forEach(n => { n.classList.add("note"); n.textContent = NOTE; });
  document.querySelectorAll("[data-kit-tele]").forEach(n => n.innerHTML = `DEMO ${String(i + 1).padStart(2, "0")} / <b>${(DEMOS[i] || ["", ""])[1].toUpperCase()}</b> &nbsp; STATUS <b id="kit-status">${status}</b>`);
  const f = document.createElement("footer"); f.className = "kit-foot tele";
  if (i >= 0) f.innerHTML = `SOURCE <a href="https://github.com/obviouslogic-ai/${current}">github.com/obviouslogic-ai/${current}</a> &nbsp; / &nbsp; PAGE demos.obviouslogic.ai/${current} &nbsp; / &nbsp; <a href="https://obviouslogic.ai">obviouslogic.ai</a>`;
  document.body.append(f);
  const tick = () => { const c = document.getElementById("kit-clock"); if (c) c.textContent = new Date().toISOString().slice(11, 19) + " UTC"; };
  tick(); setInterval(tick, 1000);
  const io = new IntersectionObserver(es => es.forEach(e => e.isIntersecting && e.target.classList.add("in")), { threshold: .1 });
  document.querySelectorAll(".screen").forEach(s => io.observe(s));
}
export const setStatus = s => { const n = document.getElementById("kit-status"); if (n) n.textContent = s; };
export const revealAll = () => document.querySelectorAll(".screen").forEach(s => s.classList.add("in"));
