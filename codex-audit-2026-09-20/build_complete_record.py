"""Build the signed, self-contained history of the fourteen-module audit."""

from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DELTA = HERE / "delta-audit-2026-09-22"
OUT = HERE / "COMPLETE_AUDIT_AND_REVISION_RECORD.html"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def clean(value: object) -> str:
    return str(value).replace("�", "–").strip()


def esc(value: object) -> str:
    return html.escape(clean(value), quote=True)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


old = load(HERE / "findings.json")
manifest = load(HERE / "revised-modules" / "build-manifest.json")
cert = load(HERE / "textbook-edition-20-rule" / "certification-report.json")
edition_manifest = load(HERE / "textbook-edition-20-rule" / "build-manifest.json")
delta_findings = load(DELTA / "findings.json")
delta_integrity = load(DELTA / "original-module-hashes.json")
mechanical = load(DELTA / "mechanical-rubric-checks.json")
rules = (HERE / "AUDIT_RUBRIC.md").read_text(encoding="utf-8").split("## A. Twenty-rule prose standard", 1)[1].split("## B.", 1)[0]

assert len(old["content"]) == 40
assert len(old["prose"]) == 48
assert len(delta_findings) == 11
assert len(manifest["modules"]) == len(cert["modules"]) == 12
assert len(delta_integrity["files"]) == 14
assert sum(x["36_to_50"] + x["over_50"] for x in mechanical["sentence_stats_by_module"].values()) == 782

for number in range(1, 15):
    name = f"module{number:02}.html"
    original = ROOT / "afd" / name
    assert digest(original) == delta_integrity["files"][f"afd/{name}"]["sha256"]
    if number <= 12:
        revised_entry = manifest["modules"][number - 1]
        assert revised_entry["module"] == number
        assert digest(HERE / "revised-modules" / name) == revised_entry["revised_sha256"]
        entry = edition_manifest["modules"][number - 1]
        assert entry["module"] == number
        assert digest(HERE / "textbook-edition-20-rule" / name) == entry["sha256"]

old_by_id = {x["id"]: x for x in old["content"]}
delta_by_module = {13: [x for x in delta_findings if x["module"] == "afd/module13.html"],
                   14: [x for x in delta_findings if x["module"] == "afd/module14.html"]}

modules = {
    1: ("Why a fluid at all?", "The fluid approximation needs a stated kinetic closure. The revision treats collision counts as a travel-time question and allows collisionless collective dynamics instead of declaring every non-collisional system non-fluid.", "The original spatial path integral was read as a proton's collision history, while a static mean free path does not include the time spent in the flow. The audit also found that calling the kinetic equation exact concealed modelling assumptions.", "The mean-free-path examples and the hierarchy from kinetic theory to moments."),
    2: ("Conservation laws", "The revision keeps the moment derivations, corrects the density dependence hidden in Reynolds number, and separates population means, medians and bounds.", "A fitted mean is not a bound on individual measurements, and a collision length can carry the density dependence even when a formula appears to cancel it.", "Integration by parts and the material-derivative chain rule."),
    3: ("Hydrostatic structure", "The revision limits the precision claim for hydrostatic balance and explains what analytic Lane–Emden checks actually test.", "A low luminosity does not bound every dynamical departure from equilibrium at the quoted precision. Agreement on special polytropes cannot serve as an error bar for all indices.", "The Lane–Emden sequence and comparison with a tabulated solar model."),
    4: ("Sound and stellar oscillations", "The revision distinguishes small instantaneous wave amplitude from cumulative nonlinear steepening and repairs related prose and cross-references.", "A weak wave can still form a shock after enough propagation. An amplitude condition alone is not a lifetime or distance bound.", "Acoustic travel time as the route to stellar frequency spacing."),
    5: ("Gravitational instability", "The revision corrects the L694-2 source claim, a dimensionless figure caption, a dependency on earlier self-gravity, and an overgeneral uncertainty claim.", "The cited source did not establish the asserted stellar classification. A figure using dimensionless axes cannot have a dimensional slope; one comparison of reconstructions cannot be a universal error floor.", "The distinction between a fitted density profile and an independent observation."),
    6: ("Convection and thermal instability", "The revision separates an effective equation-of-state parameter from conserved composition, qualifies solar-boundary estimates, and reframes a reused velocity as a consistency check.", "A closure parameter cannot be advected as if it were composition. Reusing an observed velocity to build the input flux weakens the independence of a later comparison with that velocity.", "Parcel arguments and the explicit assumptions behind the granulation estimate."),
    7: ("Interface instabilities", "The revision presents boundary conditions as the new ingredient, repairs the cross-module Jeans link, and limits what a scaling fit demonstrates.", "A fitted scaling cannot prove universal loss of initial-condition dependence; the earlier Jeans chapter already established wavelength-dependent growth.", "The common dispersion relation and its limiting cases."),
    8: ("Shocks and blast waves", "The revision distinguishes shocks from contacts, withdraws an invalid shell-width bound, and treats the Trinity comparison through an error budget.", "The planar mixing law assumes constant acceleration. Substituting the shell's instantaneous deceleration does not calculate accumulated mixing. A formal rejection level needs a complete error model.", "Conservation-law jump conditions and the Sedov derivation."),
    9: ("Winds and accretion", "The revision fixes the direction of Faraday-rotation inequalities, distinguishes X-ray band luminosity from bolometric efficiency, and clarifies transonic branch selection.", "An accretion estimate above a lower limit satisfies it; it is not refuted by it. A band luminosity divided by an outer supply rate is not the efficiency of gas reaching the black hole.", "Critical-point calculations and sensitivity to coronal base temperature."),
    10: ("Turbulence", "The revision corrects the lognormal median/mode distinction, mean-versus-median labels, energy language, and the conditional hydrostatic mass-bias interpretation.", "Dissipation converts kinetic energy into internal energy. A mass-bias estimate under chosen assumptions is not an observational confirmation, and statistical transformations must preserve the correct density measure.", "Component counting and the assumptions visible in the mass-bias derivation."),
    11: ("Accretion discs", "The revision distinguishes circularisation radius from ballistic pericentre, limits Rayleigh stability to its setting, and repairs an inherited luminosity comparison.", "Gas on a parabolic orbit can pass inside the circularisation radius without first losing angular momentum. Rayleigh stability does not exclude magnetorotational transport.", "Stress and angular-momentum transport equations."),
    12: ("Magnetohydrodynamics", "The revision reverses the mistaken mass-to-flux interpretation, separates plasma beta from Alfvén Mach number, and makes the viscosity comparison one-sided.", "Subcritical clouds have relatively stronger magnetic support. An upper bound on effective cluster viscosity does not exclude a smaller local perpendicular coefficient, and magnetic Reynolds number is not material conductivity.", "Magnetic pressure and tension, with explicit limits on classical transport coefficients."),
    13: ("Radiation hydrodynamics", "The audit proposes a qualified photospheric leakage estimate, a Thomson-regime limit for electron scattering, and a composition-dependent Eddington example. A revised module has not been written.", "The diffusion closure used in the acoustic check assumes optical thickness, yet the chosen point is only 2/3 optical depth from the surface. The Thomson cross-section also falls at high photon energy.", "The column-mean versus local-opacity distinction and the force-balance derivation."),
    14: ("Numerical methods", "The audit proposes norm-specific SPH convergence language, a limited grid-resolution scaling, and a more exact account of shock-position error. A revised module has not been written.", "The maximum SPH pressure error stays near 9%, while its integrated L1 error decreases. Conservation supports convergence but does not fix a finite-grid shock position exactly.", "Conservative updates, the CFL argument, the Sod solver, and regional error analysis."),
}


def link(href: str, label: str, cls: str = "") -> str:
    return f'<a href="{esc(href)}"{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}>{esc(label)}</a>'


def old_finding_card(f: dict) -> str:
    name = f"module{f['module']:02}.html"
    return f'''<details class="finding"><summary><span class="fid">{esc(f['id'])}</span><span>{esc(f['title'])}</span><span class="severity">{esc(f['severity'])}</span></summary>
      <div class="finding-body"><p class="location">Original: {link('../afd/' + name, f'afd/{name}')}:{esc(f['line'])}</p>
      <p><b>What was wrong.</b> {esc(f['why'])}</p>
      <p><b>Why the revision matters.</b> The correction restores the stated assumptions, inference or source meaning; the separate revised copy records its application.</p>
      <details><summary>Audit replacement text</summary><pre>{esc(f['replacement'])}</pre></details>
      </div></details>'''


def new_finding_card(f: dict) -> str:
    number = 13 if "module13" in f["module"] else 14
    return f'''<details class="finding open-item"><summary><span class="fid">{esc(f['id'])}</span><span>{esc(f['title'])}</span><span class="severity">{esc(f['severity'])}</span></summary>
      <div class="finding-body"><p class="location">Original: {link(f'../afd/module{number:02}.html', f'afd/module{number:02}.html')}:{esc(f['line'])}</p>
      <p><b>Why it needs revision.</b> {esc(f['analysis'])}</p>
      <details><summary>Proposed replacement; not applied</summary><pre>{esc(f['replacement'])}</pre></details>
      </div></details>'''


def prose_card(f: dict) -> str:
    return f'''<details class="prose-item"><summary><span class="fid">{esc(f['id'])}</span><span>Module {f['module']:02} · line {esc(f['line'])}</span></summary>
    <div class="finding-body"><p><b>Original wording.</b> “{esc(f['quote'])}”</p><p><b>Diagnosis.</b> {esc(f['diagnosis'])}</p>
    <p><b>Audit rewrite.</b> {esc(f['rewrite'])}</p></div></details>'''


module_cards = []
for number in range(1, 15):
    title, what, why, retain = modules[number]
    name = f"module{number:02}.html"
    original = link(f"../afd/{name}", "Original")
    if number <= 12:
        item = manifest["modules"][number - 1]
        found = [old_by_id[fid] for fid in item["content_findings_applied"]]
        prose = [x for x in old["prose"] if x["module"] == number]
        applied = item["prose_edits_applied_before_content_replacements"]
        superseded = item["prose_edits_not_found_or_superseded"]
        status = '<span class="status done">Revised edition exists</span>'
        links = (original + link(f"revised-modules/{name}", "Scientific revision")
                 + link(f"textbook-edition-20-rule/{name}", "Twenty-rule edition"))
        record = f'''<p class="record"><b>Recorded work:</b> {len(found)} content findings incorporated; {len(prose)} line-level prose recommendations. {len(applied)} prose edits were inserted directly before the content replacements; {len(superseded)} were superseded or not found as exact matches. A later section-by-section prose rewrite produced the twenty-rule edition. The {len(item['dependent_repairs'])} related repairs are listed in the build manifest.</p>'''
        finding_html = "".join(old_finding_card(f) for f in found)
        prose_html = (f'<details class="prose-group"><summary>See this module’s {len(prose)} audit prose examples</summary>'
                      + "".join(prose_card(f) for f in prose) + "</details>")
        status_filter = "revised"
    else:
        found = delta_by_module[number]
        status = '<span class="status pending">Audit proposals only</span>'
        links = original + link("delta-audit-2026-09-22/AUDIT_REPORT.html", "Detailed audit")
        record = f'''<p class="record"><b>Recorded work:</b> {len(found)} module-specific findings, each with proposed wording. No revised Module {number} HTML exists in the Codex edition. The original manuscript was preserved.</p>'''
        finding_html = "".join(new_finding_card(f) for f in found)
        prose_html = ""
        status_filter = "pending"
    module_cards.append(f'''<article class="module" id="module-{number:02}" data-status="{status_filter}">
      <header><div class="module-number">{number:02}</div><div><h3>{esc(title)}</h3>{status}</div></header>
      <div class="module-links">{links}</div>
      <p><b>What changed or is proposed.</b> {esc(what)}</p>
      <p><b>Why.</b> {esc(why)}</p>
      <p><b>Keep.</b> {esc(retain)}</p>{record}
      <div class="finding-stack">{finding_html}</div>{prose_html}
    </article>''')

rule_items = []
for line in rules.splitlines():
    line = line.strip()
    if line and line[0].isdigit() and ". " in line:
        n, text = line.split(". ", 1)
        rule_items.append(f'<li><span class="rule-number">{esc(n)}</span>{esc(text)}</li>')
assert len(rule_items) == 20

old_severity = {}
for finding in old["content"]:
    old_severity[finding["severity"]] = old_severity.get(finding["severity"], 0) + 1

book_wide = [x for x in delta_findings if x["id"].startswith("BOOK-")]
assert len(book_wide) == 2
independent = load(DELTA / "independent-checks.json")
mean_free_path = independent["module13"]["photosphere_mean_free_path_km"]
kn_100 = independent["module13"]["kn_cross_section_over_thomson"]["100_keV"]
sph = independent["module14"]["sph_contact_norms"]
sedov = independent["module14"]["reported_sedov_shock_location_errors"]

css = r'''
:root{color-scheme:dark;--bg:#08101a;--surface:#111e2c;--surface2:#16273a;--line:#2a3e55;--ink:#eaf1f5;--muted:#abc0ca;--aqua:#83e6db;--gold:#f4c978;--red:#ff9c98;--blue:#9ec8fa}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.58 Georgia,'Times New Roman',serif}a{color:var(--aqua);text-underline-offset:.2em}a:hover{color:#fff}button,input{font:inherit}header.site{padding:4.5rem max(24px,calc((100vw - 1240px)/2)) 3.2rem;background:radial-gradient(circle at 80% 5%,#1b5b68 0,transparent 34%),linear-gradient(135deg,#10283b,#08101a 68%);border-bottom:1px solid var(--line)}.eyebrow,.micro,.status,.tabbar,.module-number,.fid,.severity,.stat-label,.key,label{font-family:Segoe UI,Arial,sans-serif}.eyebrow{text-transform:uppercase;letter-spacing:.16em;color:var(--aqua);font-size:.78rem;font-weight:700}h1,h2,h3,h4{font-family:Segoe UI,Arial,sans-serif;line-height:1.18}h1{font-size:clamp(2.6rem,6vw,5rem);letter-spacing:-.05em;max-width:940px;margin:.5rem 0 1.1rem}h2{font-size:clamp(1.75rem,3.5vw,2.6rem);letter-spacing:-.03em;margin:0 0 1.1rem}h3{font-size:1.48rem;margin:0 0 .45rem}p{margin:.75rem 0;max-width:94ch}.deck{font-size:1.18rem;color:#c8dae0;max-width:73ch}.byline{margin-top:1.7rem;color:var(--muted);font:0.93rem Segoe UI,Arial,sans-serif}nav.top{position:sticky;top:0;z-index:10;background:#0a1421ed;backdrop-filter:blur(12px);border-bottom:1px solid var(--line);overflow:auto}nav.top .inner{max-width:1240px;margin:auto;display:flex;gap:1.5rem;padding:.8rem 24px;white-space:nowrap;font:600 .87rem Segoe UI,Arial,sans-serif}nav.top a{text-decoration:none;color:#c5dee4}nav.top a:hover{color:#fff}main{max-width:1240px;margin:auto;padding:0 24px 5rem}section{padding:3rem 0;border-bottom:1px solid var(--line)}.lead{font-size:1.12rem;color:#d8e6ea}.grid{display:grid;gap:1rem}.stats{grid-template-columns:repeat(4,1fr);margin-top:2rem}.stat{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:1.2rem}.stat b{display:block;font:700 2rem Segoe UI,Arial,sans-serif;color:var(--aqua)}.stat-label{font-size:.85rem;color:var(--muted)}.two{grid-template-columns:1fr 1fr}.panel{background:var(--surface);border:1px solid var(--line);border-radius:15px;padding:1.3rem 1.5rem}.panel h3{color:var(--aqua)}.timeline{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}.step{border-top:3px solid var(--aqua);background:var(--surface);padding:1.2rem;border-radius:0 0 12px 12px}.step .date{font:700 .82rem Segoe UI,Arial,sans-serif;color:var(--gold)}.step h3{font-size:1.1rem;margin:.3rem 0}.step p{font-size:.95rem;color:#cfdee3}.note{border-left:4px solid var(--gold);background:#2a231c;padding:1rem 1.2rem;margin:1.5rem 0}.note strong{color:#ffe4ae}.source-list{display:grid;grid-template-columns:repeat(2,1fr);gap:.85rem}.source-list a{display:block;padding:.9rem 1.1rem;background:var(--surface);border:1px solid var(--line);border-radius:9px;font:600 .94rem Segoe UI,Arial,sans-serif}.controls{display:flex;flex-wrap:wrap;gap:.7rem;margin:1.25rem 0}.controls button{background:var(--surface);border:1px solid var(--line);border-radius:100px;color:var(--ink);cursor:pointer;padding:.55rem .95rem;font:600 .9rem Segoe UI,Arial,sans-serif}.controls button[aria-pressed=true]{background:var(--aqua);color:#06202a;border-color:var(--aqua)}.controls input{background:var(--surface);color:#fff;border:1px solid var(--line);border-radius:100px;padding:.55rem 1rem;min-width:min(310px,100%)}.controls input::placeholder{color:#9cb3c0}.modules{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}.module{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:1.45rem;min-width:0;scroll-margin-top:4rem}.module:target{outline:2px solid var(--aqua)}.module header{display:flex;gap:1rem;align-items:flex-start}.module-number{color:var(--aqua);background:#173941;display:grid;place-items:center;width:3rem;height:3rem;border-radius:10px;flex:none;font-weight:800}.module p{font-size:.98rem;color:#d5e3e8}.module p b{color:#fff}.status{display:inline-block;border-radius:100px;padding:.24rem .7rem;font-size:.75rem;font-weight:700}.done{background:#163b39;color:#a9f1de}.pending{background:#4a3121;color:#ffe0a1}.module-links{display:flex;flex-wrap:wrap;gap:.5rem;margin:.9rem 0 1.2rem}.module-links a{font:600 .83rem Segoe UI,Arial,sans-serif;border:1px solid #376175;border-radius:7px;padding:.38rem .6rem;text-decoration:none}.record{border-top:1px solid var(--line);padding-top:.8rem;color:var(--muted)!important}.finding-stack{margin-top:1rem}.finding,.prose-group,.prose-item{border:1px solid var(--line);border-radius:9px;margin:.48rem 0;background:#0d1a27}.finding summary,.prose-group>summary,.prose-item summary{cursor:pointer;padding:.6rem .75rem;font:600 .86rem/1.35 Segoe UI,Arial,sans-serif;display:flex;align-items:baseline;gap:.55rem}.fid{color:var(--aqua);font-size:.76rem;white-space:nowrap}.severity{margin-left:auto;color:var(--gold);font-size:.75rem;white-space:nowrap}.finding-body{border-top:1px solid var(--line);padding:.6rem .85rem 1rem}.finding-body p{font-size:.88rem;margin:.5rem 0}.finding-body .location{font-family:Segoe UI,Arial,sans-serif;color:var(--muted);font-size:.78rem}.finding-body details summary{font:600 .8rem Segoe UI,Arial,sans-serif;color:var(--aqua);cursor:pointer;padding:.5rem 0}.prose-group{background:transparent}.prose-item{margin-left:.6rem;margin-right:.6rem}.prose-item:last-child{margin-bottom:.65rem}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#07121f;padding:.8rem;border:1px solid var(--line);border-radius:7px;color:#dce9ee;font:.79rem/1.5 Consolas,monospace;max-height:440px;overflow:auto}.rules{columns:2;column-gap:2.5rem;margin:1.3rem 0;padding:0;list-style:none}.rules li{break-inside:avoid;display:flex;gap:.6rem;margin:0 0 .85rem;padding:0 .5rem .8rem 0;border-bottom:1px solid var(--line);font-size:.95rem}.rule-number{flex:none;color:var(--aqua);font-weight:800;width:1.4rem}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1.3rem 0}.comparison>div{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:1.2rem}.comparison .label{font:700 .77rem Segoe UI,Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--gold)}.comparison .after .label{color:var(--aqua)}.comparison p{font-size:.95rem}.fine{font-size:.88rem;color:var(--muted)}.audit-map{width:100%;border-collapse:collapse;margin:1.1rem 0}th,td{border-bottom:1px solid var(--line);padding:.7rem;text-align:left;vertical-align:top}th{font:700 .8rem Segoe UI,Arial,sans-serif;text-transform:uppercase;letter-spacing:.06em;color:var(--aqua)}td{font-size:.94rem}.footer{font:0.9rem/1.6 Segoe UI,Arial,sans-serif;color:var(--muted)}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}#empty{display:none;color:var(--gold);padding:2rem}strong{color:#fff}@media(max-width:900px){.timeline{grid-template-columns:repeat(2,1fr)}.stats{grid-template-columns:repeat(2,1fr)}.modules{grid-template-columns:1fr}}@media(max-width:600px){header.site{padding:3rem 20px 2.4rem}main{padding:0 18px 4rem}section{padding:2.5rem 0}.two,.source-list,.comparison,.timeline{grid-template-columns:1fr}.stats{gap:.6rem}.stat{padding:.85rem}.stat b{font-size:1.5rem}.rules{columns:1}.module{padding:1.1rem}.module h3{font-size:1.25rem}}@media print{body{color:#111;background:#fff}header.site{background:#fff;color:#111;padding:1rem 0}main{max-width:none;padding:0}nav.top,.controls{display:none}.panel,.stat,.module,.comparison>div,.step{break-inside:avoid;background:#fff;border-color:#bbb;color:#111}.module p,.step p,.lead,.deck{color:#111}a{color:#075985}.finding-body{display:block}details:not([open])>.finding-body{display:block}.rules{columns:2}}
'''
css += '.table-wrap{overflow-x:auto}.audit-map{min-width:610px}'

samples = [
    ("Module 9 · lower bounds", "The Bondi rate was said to be refuted because it exceeded a lower limit.", "The Bondi estimate exceeds the quoted Faraday-rotation lower limits. It therefore satisfies them; only applicable upper limits can constrain it, and those carry magnetic-field assumptions.", "The logical direction of an inequality changes the physical conclusion."),
    ("Module 11 · circularisation", "Inside the circularisation radius, the gas cannot go.", "The radius ℓ²/(GM) describes a circular orbit. A zero-energy ballistic orbit with the same angular momentum reaches half that radius before turning.", "Angular momentum and orbital energy play different roles."),
    ("Module 12 · magnetic support", "The introduction reversed the subcritical and supercritical sides of the critical mass-to-flux ratio.", "Below the critical mass-to-flux ratio, magnetic stress can oppose collapse across the field in the idealised geometry. Above it, magnetic support alone is insufficient.", "The sign of the threshold is central to the chapter's conclusion."),
    ("Module 13 · photospheric diffusion", "The adiabatic assumption is REFUTED at the photosphere.", "The computed parameter indicates possible radiative leakage, but the local diffusion closure is not controlled at an outward optical depth of 2/3. A damping claim needs a non-adiabatic transfer calculation.", "This is proposed wording; Module 13 has not been rewritten."),
    ("Module 14 · SPH contact", "Standard SPH REFUTED as convergent there; the repair CONFIRMED.", "The maximum error remains near 9%, while a volume-weighted L1 error falls from 0.0511 to 0.0129 over the same resolutions. State the norm before claiming convergence or non-convergence.", "This is proposed wording; Module 14 has not been rewritten."),
]

sample_html = "".join(f'''<div class="comparison"><div><div class="label">{esc(title)} · earlier claim</div><p>{esc(before)}</p></div>
<div class="after"><div class="label">Revision or proposed correction</div><p>{esc(after)}</p><p class="fine">{esc(reason)}</p></div></div>'''
                      for title, before, after, reason in samples)

book_wide_html = "".join(f'''<div class="panel"><h3>{esc(f['id'])} · {esc(f['title'])}</h3><p>{esc(f['analysis'])}</p>
<p class="fine">Status: recorded in the 22 September follow-up. Its examples refer to the original module pages; this check has not been applied as a new fourteen-module rewrite.</p></div>'''
                              for f in book_wide)

document = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Signed Codex record of the scientific audits, corrections and prose revisions of fourteen Astrophysical Fluid Dynamics modules.">
<title>Fourteen modules · Codex audit and revision record</title><style>{css}</style></head><body>
<header class="site" id="top"><div class="eyebrow">Independent editorial record · 20–22 September 2026</div>
<h1>Fourteen modules. Two audits. One revised edition in progress.</h1>
<p class="deck">A documented account of what Codex found in <em>Astrophysical Fluid Dynamics</em>, what it changed in separate copies of Modules 1–12, why those changes matter, and what remains proposed for Modules 13–14.</p>
<p class="byline">Prepared and signed by <strong>Codex — OpenAI</strong> · Source state: Git commit 9386ef7 · 22 September 2026</p></header>
<nav class="top" aria-label="Page sections"><div class="inner"><a href="#overview">Overview</a><a href="#chronology">Work done</a><a href="#modules">Fourteen modules</a><a href="#examples">Before and after</a><a href="#bookwide">New cross-checks</a><a href="#rules">Twenty rules</a><a href="#sources">Evidence and status</a></div></nav>
<main>
<section id="overview"><h2>The state of the book</h2><p class="lead">The original fourteen HTML modules remain in <code>afd/</code>. The first audit examined Modules 1–12 and found {len(old['content'])} content problems. Codex then produced corrected copies and a separate prose edition under the twenty-rule standard. The later audit examined Modules 13–14 in depth and identified {len(delta_findings)-len(book_wide)} module-specific problems, plus {len(book_wide)} book-wide findings. No rewritten Module 13 or 14 has been delivered.</p>
<div class="grid stats"><div class="stat"><b>14</b><span class="stat-label">Original modules preserved</span></div><div class="stat"><b>40</b><span class="stat-label">First-audit content findings incorporated into separate Modules 1–12 copies</span></div><div class="stat"><b>12</b><span class="stat-label">Modules in the twenty-rule prose edition</span></div><div class="stat"><b>11</b><span class="stat-label">Later findings: 9 module-specific, 2 book-wide</span></div></div>
<aside class="note"><strong>Read the status labels carefully.</strong> “Revised edition exists” refers only to Modules 1–12 in Codex’s separate folder. “Audit proposals only” means the original Modules 13–14 still contain the identified issues. The 22 September all-module check was focused; it was not a new full scientific certification of Modules 1–12.</aside></section>

<section id="chronology"><h2>What was done</h2><div class="timeline">
<div class="step"><div class="date">20 September · First audit</div><h3>Diagnose the first twelve</h3><p>Read all twelve chapters, inspect important claims and sources, reproduce selected calculations, record {len(old['content'])} ranked content findings and {len(old['prose'])} line-level prose critiques. The six most serious findings block central conclusions.</p>{link('AUDIT_REPORT.html','Read signed audit')}</div>
<div class="step"><div class="date">20 September · Scientific corrections</div><h3>Build separate copies</h3><p>Apply all {len(old['content'])} content findings to <code>revised-modules/</code>, with dependent repairs to figures, captions, exercises or related paragraphs where needed. The original <code>afd/</code> pages stay intact.</p>{link('revised-modules/index.html','Open revised copies')}</div>
<div class="step"><div class="date">21 September · Prose edition</div><h3>Rewrite Modules 1–12</h3><p>Rewrite the revised copies under the twenty rules. The editorial certification reports no sentences above 50 words, with 119 sentences of 36–50 words retained after review. Mathematics, figures, anchors and scripts were preserved.</p>{link('textbook-edition-20-rule/index.html','Open prose edition')}</div>
<div class="step"><div class="date">22 September · New audit</div><h3>Audit Modules 13–14</h3><p>Apply the full rubric to the new chapters and the newly explicit checks to the earlier originals. Record two blocking and seven other module-specific findings, plus two book-wide findings. Proposed replacements remain unapplied.</p>{link('delta-audit-2026-09-22/AUDIT_REPORT.html','Read follow-up audit')}</div></div></section>

<section id="modules"><h2>What changed, module by module</h2><p class="lead">Each module card states the scientific or editorial correction and its reason. Expand a finding for the audit's full explanation and proposed text. The separate twenty-rule edition is the final available Codex wording for Modules 1–12.</p>
<div class="controls" role="group" aria-label="Filter modules"><button type="button" data-filter="all" aria-pressed="true">All 14</button><button type="button" data-filter="revised" aria-pressed="false">Revised 1–12</button><button type="button" data-filter="pending" aria-pressed="false">Audit only 13–14</button><label class="sr-only" for="module-search">Search modules and findings</label><input id="module-search" type="search" placeholder="Search topics or finding IDs"></div>
<div class="modules">{''.join(module_cards)}</div><p id="empty" role="status">No modules match this filter.</p></section>

<section id="examples"><h2>Why these revisions alter the meaning</h2><p class="lead">These five examples show the difference between a stylistic adjustment and a corrected physical inference. The last two are audit proposals and have not been applied to the source chapters.</p>{sample_html}</section>

<section id="bookwide"><h2>Findings that cross chapter boundaries</h2><div class="grid two">{book_wide_html}</div><p class="fine">The later mechanical screen counted 782 sentences above 35 words in the original fourteen modules. That count comes from a heuristic parser and is a triage measure, not a judgment that every long sentence is defective. The separate twenty-rule edition of Modules 1–12 was checked with its own editorial validator; its sentence counts are a different population and should not be read as a direct before/after experiment.</p></section>

<section id="rules"><h2>The twenty-rule prose standard</h2><p>The standard governs natural textbook English, paragraph logic, qualified claims, scientific transitions, symbol definitions, source separation and preservation of the originals. It sits within a wider rubric for derivations, numerical checks, evidence, pedagogy, notation and HTML production.</p><ol class="rules">{''.join(rule_items)}</ol><p>{link('AUDIT_RUBRIC.md','Read the full audit rubric')} · {link('textbook-edition-20-rule/EDITORIAL_STANDARD.md','Read the edition’s wording standard')}</p></section>

<section id="sources"><h2>Evidence, validation and limits</h2><div class="grid two"><div class="panel"><h3>What was checked</h3><p>The first audit saved six primary-source PDFs and twelve independent calculations. The later audit independently checked the photospheric optical-depth scale, energy-dependent scattering, SPH pressure error in two norms, and Sedov shock-position error. The original Module 13 and 14 problem suites passed 83 and 80 checks, respectively; Module 14’s full numerical generator passed its assertions.</p><p>Both audits recorded SHA-256 hashes of the original pages. This builder rechecked all fourteen originals against the later baseline and all twelve prose-edition files against their manifest before writing this page.</p></div>
<div class="panel"><h3>What the checks do not prove</h3><p>A successful assertion proves that a computation reproduces its coded expectation. It does not make the interpretation of the computation correct. Neither audit certifies every equation, reference or exercise in the textbook. The newest evidence-classification finding also has not been applied to a new fourteen-module edition.</p><p>Older source line numbers refer to the audited snapshots. A revision can move the same argument to a different line, so use the linked finding and revised chapter together.</p></div></div>
<div class="table-wrap"><table class="audit-map"><caption class="sr-only">Selected independent numerical checks</caption><thead><tr><th scope="col">Issue</th><th scope="col">Independent result</th><th scope="col">Why it changes the claim</th></tr></thead><tbody>
<tr><td>Module 13 · photospheric diffusion</td><td>Mean free path {mean_free_path:.2f} km; outward optical depth 2/3</td><td>The local scale is small, but the radiative boundary condition remains close.</td></tr>
<tr><td>Module 13 · electron scattering</td><td>At 100 keV, Klein–Nishina / Thomson = {kn_100:.3f}</td><td>The Thomson opacity is not constant for arbitrary spectra.</td></tr>
<tr><td>Module 14 · SPH contact</td><td>Maximum error {sph[0]['max_relative_pressure_error']:.3f} → {sph[-1]['max_relative_pressure_error']:.3f}; relative L1 {sph[0]['volume_weighted_relative_L1_near_contact']:.3f} → {sph[-1]['volume_weighted_relative_L1_near_contact']:.3f}</td><td>One norm stagnates over these runs while the integrated error decreases.</td></tr>
<tr><td>Module 14 · Sedov shock</td><td>Location errors {sedov[0]:.5f} → {sedov[1]:.5f} → {sedov[2]:.5f}</td><td>Finite-resolution positions approach the exact radius; they are not exact by conservation alone.</td></tr>
</tbody></table></div>
<div class="source-list" style="margin-top:1rem">{link('AUDIT_REPORT.html','First signed audit · Modules 1–12')}{link('delta-audit-2026-09-22/AUDIT_REPORT.html','Second signed audit · Modules 13–14')}{link('revised-modules/build-manifest.json','Applied content changes by module')}{link('textbook-edition-20-rule/EDITORIAL_CERTIFICATION.md','Prose-edition certification')}{link('delta-audit-2026-09-22/independent-checks.json','New independent calculations')}{link('delta-audit-2026-09-22/integrity-verification.json','Original-file preservation check')}</div>
<p class="fine">This page is a map and explanation of the work. The linked signed audits hold the full scientific arguments, exact source locations, proposed replacement blocks and source maps. The linked chapter files hold the actual rewritten text. Structural parsing and link validation were performed for this page; no new browser-based visual check was performed.</p></section>

<footer class="footer"><p><strong>Codex — OpenAI</strong><br>Independent audit and revision record · 22 September 2026 · America/Los_Angeles</p><p>Original textbook HTML by Claude remains in <code>afd/</code>. Codex’s audited and rewritten copies are visibly separated in <code>codex-audit-2026-09-20/</code>.</p></footer></main>
<script>(()=>{{const buttons=[...document.querySelectorAll('[data-filter]')],cards=[...document.querySelectorAll('.module')],search=document.getElementById('module-search'),empty=document.getElementById('empty');let filter='all';function update(){{const q=search.value.trim().toLowerCase();let visible=0;for(const card of cards){{const show=(filter==='all'||card.dataset.status===filter)&&(!q||card.textContent.toLowerCase().includes(q));card.hidden=!show;if(show)visible++}}empty.style.display=visible?'none':'block'}}for(const button of buttons)button.addEventListener('click',()=>{{filter=button.dataset.filter;for(const b of buttons)b.setAttribute('aria-pressed',String(b===button));update()}});search.addEventListener('input',update)}})();</script>
</body></html>'''

assert document.count('class="module"') == 14
assert document.count('class="prose-item"') == 48
assert document.count('class="finding"') == 40
assert document.count('class="finding open-item"') == 9
assert "�" not in document
OUT.write_text(document, encoding="utf-8")
print(f"Wrote {OUT}: {OUT.stat().st_size} bytes; 14 modules; 40 applied findings; 48 prose examples; 9 new module findings; 2 book-wide findings")
