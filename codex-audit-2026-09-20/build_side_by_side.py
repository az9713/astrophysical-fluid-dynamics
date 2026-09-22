"""Build the README comparison index and the standalone two-pane reader."""

from __future__ import annotations

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent.parent
AUDIT = ROOT / "codex-audit-2026-09-20"
EDITION = AUDIT / "textbook-edition-20-rule"
START = "<!-- codex-side-by-side:start -->"
END = "<!-- codex-side-by-side:end -->"
TITLES = [
    "Why a Fluid at All?",
    "Continuity, Euler, Navier–Stokes, Energy",
    "Hydrostatic Equilibrium",
    "Sound Waves and Linear Perturbation Theory",
    "The Jeans Instability",
    "Convection and Thermal Instability",
    "Rayleigh–Taylor and Kelvin–Helmholtz",
    "Shocks and the Sedov–Taylor Blast Wave",
    "Bondi Accretion and the Parker Wind",
    "Turbulence",
    "Accretion Discs",
    "Magnetohydrodynamics",
    "Radiation Hydrodynamics",
    "Numerical Methods",
]


def module_data() -> list[dict]:
    record = BeautifulSoup(
        (AUDIT / "COMPLETE_AUDIT_AND_REVISION_RECORD.html").read_text(encoding="utf-8"),
        "html.parser",
    )
    modules = []
    for number, title in enumerate(TITLES, 1):
        key = f"{number:02}"
        original = ROOT / "afd" / f"module{key}.html"
        revised = EDITION / f"module{key}.html"
        left = BeautifulSoup(original.read_text(encoding="utf-8"), "html.parser")
        right = BeautifulSoup(revised.read_text(encoding="utf-8"), "html.parser")
        sections = [
            {"id": tag["id"], "title": tag.get_text(" ", strip=True)}
            for tag in left.find_all(["h2", "h3"])
            if tag.get("id") and right.find(id=tag["id"])
        ]
        if not sections:
            raise ValueError(f"No matching section anchors in module {key}")

        if number <= 12:
            card = record.find(id=f"module-{key}")
            if card is None:
                raise ValueError(f"Missing audit record for module {key}")
            paragraphs = card.find_all("p", recursive=False)
            change = next(
                (p.get_text(" ", strip=True).removeprefix("What changed or is proposed. ")
                 for p in paragraphs if p.get_text(" ", strip=True).startswith("What changed or is proposed.")),
                "See the signed audit record for the editorial changes.",
            )
            why = next(
                (p.get_text(" ", strip=True).removeprefix("Why. ")
                 for p in paragraphs if p.get_text(" ", strip=True).startswith("Why.")),
                "See the signed audit record for the scientific rationale.",
            )
        elif number == 13:
            change = (
                "The exposition now follows radiation moments, transfer, diffusion, "
                "the atmosphere and radiative force. It qualifies the photospheric "
                "leakage estimate, the opacity comparison and the Eddington example."
            )
            why = (
                "Diffusion at optical depth 2/3 is only a local estimate; a column-mean "
                "opacity is not a local opacity; and the electron-scattering formula "
                "depends on composition and the Thomson regime."
            )
        else:
            change = (
                "The exposition now follows conservation, stability, modified "
                "equations, Riemann solutions, convergence and resolution. It reports "
                "SPH error by norm and treats grid scalings as estimates."
            )
            why = (
                "The maximum SPH pressure error stays roughly constant while its "
                "volume-weighted L1 error falls. Conservation alone does not make "
                "the Sedov shock position exact on a finite grid."
            )
        modules.append({
            "number": key,
            "title": title,
            "sections": sections,
            "change": change,
            "why": why,
        })
    return modules


PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Compare the original and Codex textbook editions of all fourteen Astrophysical Fluid Dynamics modules, section by section.">
<title>Original and Codex editions | Astrophysical Fluid Dynamics</title>
<style>
:root { color-scheme: dark; --bg:#0b1420; --panel:#142336; --line:#36516b; --ink:#eef4f7; --muted:#c2d2dd; --accent:#91e7dc; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink); font:16px/1.5 system-ui,Segoe UI,sans-serif; }
a { color:var(--accent); text-underline-offset:.18em; }
a:focus-visible,select:focus-visible { outline:3px solid #f4c978; outline-offset:3px; }
header { padding:1.5rem clamp(1rem,3vw,2rem); background:#102237; border-bottom:1px solid var(--line); }
h1 { margin:.15rem 0 .4rem; font-size:clamp(1.6rem,3vw,2.3rem); line-height:1.2; }
header p { margin:.3rem 0; max-width:95ch; color:var(--muted); }
main { padding:1.1rem clamp(.7rem,2vw,1.5rem) 2rem; }
.toolbar { display:flex; flex-wrap:wrap; gap:1rem; align-items:end; margin-bottom:1rem; }
label { display:grid; gap:.3rem; font-weight:650; }
select { background:var(--panel); color:var(--ink); border:1px solid var(--line); border-radius:6px; padding:.55rem .7rem; font:inherit; max-width:min(88vw,700px); }
#module { min-width:min(88vw,390px); }
.notes { border:1px solid var(--line); border-radius:9px; background:var(--panel); padding:.8rem 1rem; margin:0 0 1rem; }
.notes p { margin:.25rem 0; }
.notes .links { margin-top:.6rem; font-size:.93rem; }
.panes { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; }
.pane { min-width:0; border:1px solid var(--line); border-radius:9px; overflow:hidden; background:#fff; }
.pane-head { display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; gap:.5rem; padding:.7rem .9rem; background:var(--panel); color:var(--ink); }
.pane-head h2 { margin:0; font-size:1rem; }
.pane-head a { font-size:.88rem; }
iframe { width:100%; height:75vh; min-height:580px; border:0; display:block; background:#fff; }
.foot { color:var(--muted); font-size:.9rem; margin:1rem 0 0; }
@media(max-width:900px) { .panes { grid-template-columns:1fr; } iframe { height:68vh; min-height:460px; } }
</style>
</head>
<body>
<header>
<h1>Original and Codex editions</h1>
<p>Read the same module in two panes. Choose a shared section to jump both pages to matching anchors. Each page scrolls independently after the jump.</p>
<p>“Original” means the audited file in <code>afd/</code>; “Codex edition” means the separate twenty-rule rewrite. The comparison does not establish which model authored the original.</p>
</header>
<main>
<div class="toolbar">
<label>Module <select id="module" aria-label="Choose module"></select></label>
<label>Matching section <select id="section" aria-label="Choose matching section"></select></label>
</div>
<section class="notes" aria-labelledby="notes-heading">
<h2 id="notes-heading" style="margin:.1rem 0 .45rem;font-size:1.1rem">What changed, and why</h2>
<p><strong>Revision:</strong> <span id="change"></span></p>
<p><strong>Reason:</strong> <span id="why"></span></p>
<p class="links"><a id="record" href="COMPLETE_AUDIT_AND_REVISION_RECORD.html">Full audit record</a> · <a id="certification" href="textbook-edition-20-rule/EDITORIAL_CERTIFICATION.md">Editorial certification</a> · <a href="../README.md">Repository README</a></p>
</section>
<div class="panes">
<section class="pane" aria-labelledby="original-heading">
<div class="pane-head"><h2 id="original-heading">Original · <span id="original-number"></span></h2><a id="original-link" target="_blank" rel="noopener">Open original page</a></div>
<iframe id="original-frame" title="Original module"></iframe>
</section>
<section class="pane" aria-labelledby="codex-heading">
<div class="pane-head"><h2 id="codex-heading">Codex edition · <span id="codex-number"></span></h2><a id="codex-link" target="_blank" rel="noopener">Open Codex page</a></div>
<iframe id="codex-frame" title="Codex revision"></iframe>
</section>
</div>
<p class="foot">The controls use only anchors present in both files. Opening links preserve the chosen section. Prepared by Codex (OpenAI), 22 September 2026.</p>
</main>
<script>
const modules = __MODULE_DATA__;
const moduleSelect = document.getElementById('module');
const sectionSelect = document.getElementById('section');
for (const item of modules) {
  const option = document.createElement('option');
  option.value = item.number;
  option.textContent = `${Number(item.number)}. ${item.title}`;
  moduleSelect.append(option);
}
function show(moduleNumber, sectionId, updateHistory) {
  const item = modules.find(entry => entry.number === moduleNumber) || modules[0];
  moduleSelect.value = item.number;
  sectionSelect.replaceChildren();
  const start = document.createElement('option');
  start.value = '';
  start.textContent = 'Start of module';
  sectionSelect.append(start);
  for (const section of item.sections) {
    const option = document.createElement('option');
    option.value = section.id;
    option.textContent = section.title;
    sectionSelect.append(option);
  }
  const selected = item.sections.some(section => section.id === sectionId) ? sectionId : '';
  sectionSelect.value = selected;
  const suffix = selected ? `#${encodeURIComponent(selected)}` : '';
  const original = `../afd/module${item.number}.html${suffix}`;
  const codex = `textbook-edition-20-rule/module${item.number}.html${suffix}`;
  document.getElementById('original-frame').src = original;
  document.getElementById('codex-frame').src = codex;
  document.getElementById('original-link').href = original;
  document.getElementById('codex-link').href = codex;
  document.getElementById('original-number').textContent = item.number;
  document.getElementById('codex-number').textContent = item.number;
  document.getElementById('change').textContent = item.change;
  document.getElementById('why').textContent = item.why;
  const record = document.getElementById('record');
  record.href = item.number >= '13'
    ? 'delta-audit-2026-09-22/AUDIT_REPORT.html'
    : `COMPLETE_AUDIT_AND_REVISION_RECORD.html#module-${item.number}`;
  record.textContent = item.number >= '13' ? 'Independent delta audit' : 'Full audit record';
  document.getElementById('certification').href = item.number >= '13'
    ? 'textbook-edition-20-rule/EDITORIAL_CERTIFICATION_13_14.md'
    : 'textbook-edition-20-rule/EDITORIAL_CERTIFICATION.md';
  if (updateHistory) {
    const url = new URL(location.href);
    url.searchParams.set('module', item.number);
    if (selected) url.searchParams.set('section', selected);
    else url.searchParams.delete('section');
    history.replaceState(null, '', url);
  }
}
moduleSelect.addEventListener('change', () => show(moduleSelect.value, '', true));
sectionSelect.addEventListener('change', () => show(moduleSelect.value, sectionSelect.value, true));
window.addEventListener('popstate', () => {
  const query = new URLSearchParams(location.search);
  show(query.get('module'), query.get('section'), false);
});
const query = new URLSearchParams(location.search);
show(query.get('module'), query.get('section'), false);
</script>
</body>
</html>
'''


def main() -> None:
    data = module_data()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    (AUDIT / "SIDE_BY_SIDE.html").write_text(
        PAGE.replace("__MODULE_DATA__", payload), encoding="utf-8"
    )

    pages = "https://az9713.github.io/astrophysical-fluid-dynamics/"
    rows = []
    for item in data:
        key = item["number"]
        title = item["title"]
        rows.append(
            f"| {int(key)}. {title} | [Read original]({pages}afd/module{key}.html) | "
            f"[Read Codex edition]({pages}codex-audit-2026-09-20/textbook-edition-20-rule/module{key}.html) | "
            f"[Compare both]({pages}codex-audit-2026-09-20/SIDE_BY_SIDE.html?module={key}) |"
        )
    block = "\n".join([
        START,
        "## Original and Codex editions: side-by-side comparison",
        "",
        "The table pairs each audited `afd/` module with its separate Codex rewrite. "
        "Choose **Compare both** for full-length, two-pane reading and matching-section navigation. "
        "The links open the rendered pages on GitHub Pages. You can also "
        "[open the comparison file locally](codex-audit-2026-09-20/SIDE_BY_SIDE.html). "
        "GitHub's README view cannot embed the interactive comparison itself.",
        "",
        "| Module | Original `afd/` | Codex twenty-rule edition | Full comparison |",
        "|---|---|---|---|",
        *rows,
        "",
        "For the scientific and editorial reasons behind the changes, see the "
        "[signed audit and revision record](codex-audit-2026-09-20/COMPLETE_AUDIT_AND_REVISION_RECORD.html). "
        "For Modules 13–14, also see the "
        "[later editorial record](codex-audit-2026-09-20/textbook-edition-20-rule/EDITORIAL_CERTIFICATION_13_14.md), "
        "which supersedes the older record's statement that those two rewrites were pending. "
        "This comparison labels the `afd/` files as originals; it does not independently establish their model authorship.",
        END,
    ])
    readme = ROOT / "README.md"
    contents = readme.read_text(encoding="utf-8")
    if START in contents and END in contents:
        contents = re.sub(re.escape(START) + r".*?" + re.escape(END), block, contents, flags=re.S)
    elif "## Contents" in contents:
        contents = contents.replace("## Contents", block + "\n\n## Contents", 1)
    else:
        raise ValueError("Could not locate the README contents heading")
    readme.write_text(contents, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
