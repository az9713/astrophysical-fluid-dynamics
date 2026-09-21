from pathlib import Path
from bs4 import BeautifulSoup
import json,html
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
d=json.loads((OUT/'findings.json').read_text(encoding='utf8'))
F,P=d['content'],d['prose']
inv=json.loads((OUT/'coverage-inventory.json').read_text(encoding='utf8'))
mechanical=json.loads((OUT/'mechanical-checks.json').read_text(encoding='utf8'))
e=html.escape
T=chr(96)
body=[]; md=[]
def heading(title,id,level=2):
 body.append(f'<h{level} id="{id}">{e(title)}</h{level}>')
 md.extend(['#'*level+' '+title,''])
def para(t):
 body.append('<p>'+e(t)+'</p>');md.extend([t,''])
def loc(m,n):
 soup=BeautifulSoup((ROOT/'afd'/f'module{m:02}.html').read_bytes().decode('utf8'),'html.parser')
 ids=[x for x in soup.find_all(id=True) if x.sourceline and x.sourceline<=n]
 anchor='#'+ids[-1]['id'] if ids else ''
 return f'<a href="../afd/module{m:02}.html{e(anchor)}">module{m:02}.html:{n}</a>'

heading('Independent scientific and prose audit','top',1)
para('Astrophysical fluid dynamics · Written Modules 01–12')
para('Signed: Codex — OpenAI | 20 September 2026 | America/Los_Angeles')
body.append('<div class="stats"><div><strong>12</strong>modules surveyed</div><div><strong>40</strong>content findings</div><div><strong>48</strong>prose rewrites</div><div><strong>0</strong>original files edited</div></div>')
heading('Verdict: substantial revision required','verdict')
para('Yes, after substantial revision. The twelve written modules contain enough useful derivation and physical material to form a good textbook, but the present manuscript is not ready to be relied on as one. Several central conclusions are mathematically or logically wrong; the most serious errors concern observational bounds, magnetic support, accretion and time-dependent mixing. The prose is frequently grammatical yet unnatural, repetitive and unnecessarily combative. It often explains the manuscript’s production history instead of the physics. A cosmetic copy-edit would leave these problems intact.')
heading('Scope and method','scope')
for t in [
'This is an independent report by Codex, not an amendment to Claude’s manuscript or a claim to represent a human publisher. It applies the named science-editor skill to the current local checkout. Findings are examples supported by evidence, not an estimate of the percentage of all sentences or claims that are defective.',
'Snapshot: Git HEAD f93735fd035d4fd6e01376ad8415b61c54732709, including the working-copy changes already present in module10.html and module12.html. The existing untracked afd-stem-textbook-runbook.html was preserved. Line numbers refer to this local snapshot, not necessarily the current GitHub page. The public repositories were opened for context; the local manuscript is the object of the audit.',
'All twelve written modules were surveyed: their main narrative, definitions, major results, figures and captions, conclusions, and selected proofs and exercises. High-consequence claims and cross-module inconsistencies were pursued in detail. This is not a fresh derivation of every proposition, a solution of every exercise, a complete numerical reproduction, or certification of every reference. No previous editor’s pass/fail verdict was treated as evidence of correctness.',
'The domain brief was assembled from README.md, HANDOFF.md, the current modules, and the project’s house-style and notation documents under .ignore/plan. The reader is mathematically mature but new to the subfield; the book uses Gaussian/CGS conventions. Historical memory was used only to orient the inspection; current files determined the findings.',
'Six primary-source PDFs were downloaded into this audit folder and relevant passages were read. Twelve independent algebraic or numerical checks were saved separately. Local links were checked across the modules. The preservation check found all twelve module files unchanged from the audit baseline. Of 217 original files, 216 retained their hashes; HANDOFF.md changed while the checkout advanced to commit ff289c4c345a3dd83ebfdc7ef9c57384e3534515. These changes were outside Codex’s audit actions. Codex wrote only inside this new audit folder and did not restore or modify the concurrent changes. See integrity-verification.json.',
'The 40 replacements below are complete proposed paragraphs or result boxes, not a complete patch for every repeated occurrence, table, figure or exercise. No replacement was applied. The 48 prose edits are representative rather than a full copy-edit. The inventory contains about 164,000 whitespace-separated text tokens, including mathematical notation; that is not a count of ordinary English words.'
]:para(t)

heading('Ranked content findings','findings')
para('The first six findings block reliance on central conclusions. Major findings teach an incorrect concept, inference or scope. Moderate findings affect precision, consistency or validation. Quotes and locations are taken from the current HTML; each proposed replacement is separate from the original.')
body.append('<div class="filters"><label>Module <select id="module-filter"><option value="">All</option>'+''.join(f'<option value="{i}">{i:02}</option>' for i in range(1,13))+'</select></label><label>Severity <select id="severity-filter"><option value="">All</option><option>Blocking</option><option>Major</option><option>Moderate</option></select></label><button id="reset" type="button">Show all</button><span id="count" aria-live="polite"></span></div>')
rank={'Blocking':0,'Major':1,'Moderate':2}
for f in sorted(F,key=lambda x:(rank[x['severity']],int(x['id'][1:]))):
 m,n=f['module'],f['line']
 body.append(f'<article class="finding" data-module="{m}" data-severity="{f["severity"]}" id="{f["id"]}"><div class="meta"><span class="severity {f["severity"].lower()}">{f["severity"]}</span> {f["id"]} · {loc(m,n)}</div><h3>{e(f["title"])}</h3><blockquote>{e(f["quote"])}</blockquote><p>{e(f["why"])}</p><p class="small"><b>Standard affected:</b> {e(f["standard"])}<br><b>Evidence:</b> {e(f["basis"])}</p><div class="replacement"><h4>Proposed replacement — not applied</h4>{f["replacement"]}</div><details><summary>Copyable replacement HTML</summary><pre><code>{e(f["replacement"])}</code></pre></details></article>')
 md.extend([f'### {f["id"]} — {f["severity"]}: {f["title"]}','',f'Location: afd/module{m:02}.html:{n}','',f'> {f["quote"]}','',f['why'],'','Standard affected: '+f['standard'],'','Evidence: '+f['basis'],'','**Proposed replacement — not applied:**','',T*3+'html',f['replacement'],T*3,''])

heading('Prose and clarity','prose')
for title,t in [
('The objection is justified, but “bad grammar” is too narrow.',
'There are genuine local errors: “The Coulomb force has no range” says the wrong thing; the photospheric “—, against” construction mishandles punctuation; a radius is described as the size “across”; and the list of “all different” powers repeats k². Many other sentences are syntactically legal. Their problems are register, reference, rhythm or meaning. Calling all of them ungrammatical would obscure the work that actually needs doing.'),
('The dominant voice is a referee delivering verdicts.',
'“Confirmed”, “refuted”, “the premise is spent” and “what the gap indicts” make the author sound preoccupied with winning an argument. A textbook should distinguish a derivation, a numerical check, a fitted parameter, a consistency comparison and a falsification. Those categories are repeatedly blurred. The reversed-bound examples show that this is more than an aesthetic problem.'),
('The book repeatedly explains its own manufacture.',
'The reader encounters “first draft”, “shipped page”, “Gate D”, generators, what was fetched, and debts owed to other modules. Reproducibility and provenance matter, but most of this belongs in an editorial log, source appendix or reproducibility note. The physical argument should survive removal of every sentence about how the chapter was produced.'),
('The recurring metaphors require an unnecessary translation.',
'Assumptions are paid for or spent; modules owe and repay; gravity charges and shear pays; discrepancies indict models. An occasional analogy can help. This repeated financial and adversarial vocabulary forces the reader to translate physics into the author’s private idiom. State the mechanism, approximation or comparison directly.'),
('Prominent claims outrun their own caveats.',
'“Exactly”, “nothing else”, “every” and “cannot” repeatedly extend conclusions beyond their assumptions. Some subsequent paragraphs provide good qualifications, but a correct caveat does not cure a false opening or result box. Readers reasonably remember the prominent sentence. Its condition belongs in that sentence.'),
('The rhythm exposes the template.',
'A setup announces a disagreement; a bold sentence declares a result; a calculation returns a striking ratio; a paragraph confirms or refutes; a final sentence passes a debt to another module. This repetition, alongside stage directions such as “Hold that number”, creates the artificial effect the user noticed. This is a stylistic diagnosis, not an AI-authorship detector or a claim about Claude’s hidden drafting process.'),
('The skill’s appearance is present; its central judgement is inconsistent.',
'The science-editor skill requires precise claims, defined terms, proofs, limits and evidence. The manuscript often has their outward forms—proposition boxes, algebra and source quotations—but important inferences still fail. A script can confirm that 8.02×10⁻⁶ divided by 2×10⁻⁸ is 401 without checking whether exceeding a lower bound is a contradiction. That semantic check is the missing editorial work. Conversely, mechanically applying a five-part template to every simple identity can inflate the prose. Not every connective step needs a proposition box.'),
('Numerical precision is not the same as physical precision.',
'Many digits can be useful for checking a numerical implementation against an analytic case. They should not be carried uncritically into conclusions based on uncertain astrophysical inputs. The book sometimes makes this distinction well, then abandons it in the next verdict. State separately the numerical error, measurement error and model uncertainty.')
]:
 heading(title,'diagnosis-'+str(len(body)),3);para(t)
heading('48 representative line edits','line-edits',3)
para('Each edit identifies whether the issue is incorrect English, ambiguity, overstatement or stylistic choice. The revisions preserve mathematical depth while replacing theatrical or administrative language with explanation.')
for m in range(1,13):
 heading(f'Module {m:02}',f'prose-{m}',3)
 for p in [p for p in P if p['module']==m]:
  body.append(f'<article class="prose-edit"><div class="meta">{p["id"]} · {loc(m,p["line"])}</div><blockquote>{e(p["quote"])}</blockquote><p><b>Diagnosis.</b> {e(p["diagnosis"])}</p><p class="rewrite"><b>Rewrite.</b> {e(p["rewrite"])}</p></article>')
  md.extend([f'**{p["id"]} — module{m:02}.html:{p["line"]}**','',f'> {p["quote"]}','',p['diagnosis'],'','**Rewrite:** '+p['rewrite'],''])

heading('Module-by-module assessment','modules')
para('Every written module was surveyed. The strengths below identify useful material; they do not certify every calculation in that module.')
modules=[
('Why a fluid at all?','A strong opening question is undermined by an “exact” Boltzmann equation, an over-rigid fluid definition, the collision-age inference and the claim of unchanging galactic orbits. Rebuild the hierarchy from kinetic models to moments and closures, identifying what collisions, fields and scale separation each justify.','The neutral and Coulomb mean-free-path mechanisms and the explanation of reciprocal averaging.','C08, C15, C16, C34'),
('Conservation laws','Keep the moment derivations but rewrite their interpretations. Re retains density dependence through the collision length; separate population fits do not bound the mean mass flux. Clarify scalar/vector equation counting and reconcile the promised μ/μₘ convention across the book.','The integration-by-parts steps and explicit material-derivative chain rule.','C07, C29, C36'),
('Hydrostatic structure','The luminosity-based precision claim is invalid even though hydrostatic equilibrium is a sound mean-structure approximation. Separate dynamical and secular timescales. Recast the atmospheric reference profile and distinguish analytic numerical checks from error estimates for other indices.','The Lane–Emden development and comparison between simplified polytropes and the real Sun.','C09, C18 (also applies here), C37'),
('Sound and stellar oscillations','Comparatively close to a coherent teaching chapter, but the small-amplitude argument omits cumulative nonlinear steepening. Historical flourishes, numerical values used as grammatical subjects and stale forward references interrupt the explanation.','The connection between acoustic travel time and stellar frequency spacing.','C17; C35 and P16 for the ionisation reference'),
('Gravitational instability','Introduce perturbed self-gravity rather than self-gravity for the first time. Repair the dimensionless figure caption, the L694-2 classification and the universal mass-error claim. Distinguish the Jeans infinite-medium setting from finite pressure-confined equilibria before comparing their criteria.','The careful distinction between a fitted/reconstructed contrast and an independent observation.','C14, C27, C35, C38'),
('Convection and thermal instability','The parcel arguments are useful, but the solar stability conclusions outrun the thermodynamic information supplied. Separate effective equation-of-state parameters from conserved composition, approximate evaluations from precise boundaries, and consistency checks from independent predictions.','The explicit density, correlation and formation-height assumptions in the granulation-flux calculation; carry them into the verdict.','C10, C18, C19, C40'),
('Interface instabilities','The common dispersion relation is a good organising device. Boundary conditions are the new ingredient, not wavelength-dependent growth itself. Replace the financial metaphors; distinguish scaling form from universal coefficient and wavelength dependence from selection of a finite fastest-growing scale.','The limiting cases and the distinction between a sufficient Richardson-number condition and its converse.','C20, C31'),
('Shocks and blast waves','Requires scientific repair before polish. Distinguish shocks from contacts, rebuild the Trinity comparison around an error budget, and withdraw the shell mixing-width bound until acceleration history and geometry are handled. Two malformed TeX source fragments also need repair.','Conservation-law jump derivations and the refusal to compare a gas-dynamic prediction with an incompatible magnetic-shock Mach number.','C03, C21, C28; production notes'),
('Winds and accretion','The critical-point calculations are valuable. The principal observational refutation fails because a lower bound is used backwards; the luminosity comparison adds a separate invalid rejection. Clarify the branch selection and separate outer supply, inner accretion, band luminosity and bolometric efficiency.','The analysis of exponential sensitivity to base temperature and the warning that a factor-of-few mass-loss match is a weak test.','C01, C05, C22, C23'),
('Turbulence','Replace unsupported absolutes about energy destruction, exact results and density statistics. Correct the lognormal variable transformation. Keep the assumptions of the hydrostatic mass-bias theorem in its result box. Fix the mean/median table label and six-year chronology.','The component-counting discipline and the explicit derivative caveat in the mass-bias proof.','C11, C24, C30, C39'),
('Accretion discs','Begin with orbital energy and angular momentum as distinct constraints. Circularisation is not a hard ballistic stopping radius. State Rayleigh stability in its limited setting, correct the α inequality, and repair the inherited luminosity comparison.','The distinction between Newtonian and relativistic efficiency values and the development of the stress/transport equations.','C05 (inherited), C06, C12, C25'),
('Magnetohydrodynamics','Several central interpretations need repair: critical mass-to-flux direction, beta versus Alfvén Mach number, and the viscosity-bound inference. Replace the promise-ledger introduction with magnetic stress, induction and wave speeds. Distinguish particle magnetisation, pressure ratio and bulk-flow response.','The magnetic-pressure/tension decomposition and explicit warnings about applying classical coefficients outside their regimes.','C02, C04, C13, C26, C32, C33')
]
for i,(title,critique,strength,refs) in enumerate(modules,1):
 body.append('<article class="module-card">')
 heading(f'{i:02} · {title}',f'module-{i}',3)
 para(critique);para('What to preserve: '+strength);para('Relevant findings: '+refs+'.')
 body.append(f'<p class="small">{inv[i-1]["lines"]:,} source lines · {inv[i-1]["words"]:,} approximate text tokens · <a href="#prose-{i}">Prose edits</a></p></article>')

heading('Structure and pedagogy','structure')
for title,t in [
('Use a physical sequence instead of a production ledger.','Question → assumptions → derivation → interpretation → worked example → limits. Move fetched-source status, previous-draft corrections, gate names, generator details and cross-module debts into supporting notes. Keep reproducibility links without narrating the build process in the explanation.'),
('Replace the binary verdict system.','Distinguish “derived under these assumptions”, “implementation check”, “fit”, “conditional consistency comparison”, “observational constraint” and “rejected under a stated error model”. A discrepancy does not automatically reject a theory; reproducing an input-derived number does not independently confirm one.'),
('Keep assumptions in summaries, captions and exercises.','Module 10 shows how a correct conditional theorem can become a false unconditional teaching point. When revisions are authorised, repair every dependent summary, figure caption, accessibility description, table and solution, not just the main paragraph.'),
('Repair the dependency map.','Module 3 already uses self-gravity; Module 6 develops partial-ionisation thermodynamics. Modules 11 and 12 discuss each other’s drafting order instead of presenting a clean reading order. Planned topics should be visibly labelled as planned, not offered as working links. Promised two-temperature and anisotropic-plasma material should be delivered or explicitly excluded at the relevant first use.'),
('Distinguish uncertainty from disagreement.','A model-to-model difference is not an uncertainty interval; a lower limit is not a point measurement; a local tensor coefficient is not an observational effective scalar. Identify the measured and derived quantities, the assumptions connecting them and the errors before printing a ratio.'),
('Use exercises to teach judgement.','Retain substitution exercises but add questions that require a limiting case, a probability-density transformation, the direction of an observational bound, or identification of a missing assumption. These mechanisms catch the actual errors found here. The complete exercise set was not independently solved in this audit.'),
('Reduce repetition without reducing the mathematics.','The reader can handle full derivations. Cut repeated self-justification: the proposition announces a result, the proof derives it, the paragraph restates it emphatically and the verdict announces it again. Keep a repetition only if it adds a new physical interpretation or example.')
]:
 heading(title,'structure-'+str(len(body)),3);para(t)
heading('Demonstrations of a more natural opening','openings',3)
for title,pars in [
('Module 9',[
'Gas around a gravitating body need not remain in hydrostatic equilibrium. A hot corona can expand as a wind, while gas supplied at large radius can flow inward. We will study both possibilities using steady spherical flow. The geometry simplifies the equations enough that we can trace how pressure, gravity and inertia determine the radial velocity.',
'The central difficulty occurs where the flow speed equals the sound speed. At that point, a smooth solution requires the numerator of the velocity equation to vanish along with its denominator. We will derive this regularity condition, distinguish the wind and accretion branches, and ask which observational comparisons constrain the idealised solutions.']),
('Module 12',[
'A magnetic field changes a conducting fluid in two related ways: it exerts stresses on the gas, and the moving gas changes the field. We begin by deriving the magnetic force and the induction equation. Together with mass, momentum and energy conservation, they define the magnetohydrodynamic model used in this chapter.',
'Three comparisons will recur. Plasma beta compares thermal with magnetic pressure. The Alfvén Mach number compares the flow speed with an Alfvénic wave speed. The product of gyrofrequency and collision time measures how strongly particles respond to the field between collisions. These quantities answer different questions, so we will keep their roles separate when discussing waves, collapse, transport and disc instability.'])
]:
 body.append('<div class="replacement">');heading(title,'opening-'+title.replace(' ','-'),4)
 for t in pars:para(t)
 body.append('</div>')

heading('Production checks and audit limits','production')
for t in [
'The local-link check found eight unresolved destinations: seven links to unwritten Modules 13 or 14 and one missing anchor in Module 2. These are current filesystem checks, not an external-link availability survey. No live website was changed.',
'Module 8’s caption at lines 303–305 splits the intended rho commands into new lines followed by “ho_2” and “ho_1”. At lines 938–939, an intended roman BW subscript is split into a newline followed by “m BW”. These are malformed source fragments, not ordinary line wrapping. The intended first expression is $\\rho_2/\\rho_1 = \\mathcal{M}^2 = \\gamma M_1^2$; the second affected token is $R_{\\rm BW}$. Both need rendering verification after an authorised repair.',
'The twelve independent checks test particular audit arguments, not the entire textbook. They cover Reynolds scaling, oscillatory acceleration, buoyancy periods, time-dependent mixing, bound logic, the lognormal mode, ballistic pericentre, the α inequality, beta versus Mach number, radial decades and gyro-orbit counting. No existing generator or build script was run to rewrite textbook outputs.',
'Rhetorical counts are saved in mechanical-checks.json. They describe extracted text after removing scripts, styles and SVG, and include quoted material. They are not a quality score or an AI-authorship score.',
'The report uses the manuscript’s optional MathJax CDN for display. Its text, source evidence, copyable replacement HTML and Markdown companion remain available without mathematical rendering.'
]:para(t)
body.append('<div class="table-wrap"><table><thead><tr><th>Source</th><th>Unresolved destination</th></tr></thead><tbody>')
for x in mechanical['broken_local_links']:
 body.append(f'<tr><td>{e(x["file"])}:{x["line"]}</td><td>{e(x["href"])}</td></tr>')
 md.append(f'- {x["file"]}:{x["line"]} → {x["href"]}')
body.append('</tbody></table></div>');md.append('')

heading('Evidence and source map','sources')
para('PDF page numbers count from one. Files and SHA-256 hashes are retained in the evidence folder. Only the identified passages were independently checked for this report; this is not a complete audit of the cited papers.')
sources=[
('marrone2007',4,'Marrone et al. (2007): Sgr A* rotation measure','https://arxiv.org/abs/astro-ph/0611791','Read the lower-limit paragraph and field-strength caveats. The source says lower limits “may pose problems for very low” accretion-rate models. Used for C01.'),
('zhuravleva2019',5,'Zhuravleva et al. (2019): cluster viscosity','https://arxiv.org/abs/1906.06346','Read pp. 4–5 and p. 12, including the anisotropic-transport alternative. The key direction is “suppressed by at least a factor”. The constraint is one-sided and depends on the Prandtl number. Used for C02.'),
('kandori2005',5,'Kandori et al. (2005): globule structure','https://arxiv.org/abs/astro-ph/0506205','Read §2.1. Barnard 335 has a Class 0 source; L694-2 “shows strong evidence of gas inward motion”, the stated classification basis. Used for C14, without making a claim about all later observations.'),
('troland2008',2,'Troland & Crutcher (2008): magnetic fields in cores','https://arxiv.org/abs/0802.2253','Read pp. 2–3. Subcritical masses satisfy M < MΦ; the opposite side is supercritical. Used for C04.'),
('king2007',6,'King, Pringle & Livio (2007): disc viscosity','https://arxiv.org/abs/astro-ph/0701803','Read the simulation summary on p. 4 and discussion on p. 6: observational α ≈ 0.1–0.4 versus simulated α ≤ 0.02 in the stated comparison. Used for C12, not as a survey of modern MRI simulations.'),
('venzheimer2018',8,'Venzmer & Bothmer (2018): solar-wind distributions','https://arxiv.org/abs/1711.07534','Read Table 3 and its separate Median and Mean headers. The values reproduced in Module 10 are from the mean column. Used for C30. The local evidence filename retains the downloader’s spelling.')
]
for sid,page,title,url,note in sources:
 body.append(f'<article class="source"><h3><a href="{url}">{e(title)}</a></h3><p><a href="sources/{sid}.pdf#page={page}">Local PDF, page {page}</a> · <a href="sources/{sid}.txt">Extracted text</a></p><p>{e(note)}</p></article>')
 md.extend([f'- [{title}]({url}). Local sources/{sid}.pdf, p. {page}. {note}',''])
for title,url,note in [
('Verscharen et al. (2019), equation 133','https://link.springer.com/article/10.1007/s41116-019-0021-0','The collisional-age definition follows a plasma element, ∫dt/τ = ∫dr/(Uτ). Read on the source page; used for C08.'),
('MIT OCW 2.57 lecture notes','https://ocw.mit.edu/courses/2-57-nano-to-macro-transport-processes-spring-2012/2e4ecaa5cf55f03bcefbc8ccce79aed6_MIT2_57S12_lec_notes_2004.pdf','Supporting exposition for the collision-model assumptions in C15, including molecular chaos; not a full audit of the notes.'),
('Textbook repository','https://github.com/az9713/astrophysical-fluid-dynamics','Opened for context. The local working-copy files were audited.'),
('Writing-skills repository','https://github.com/az9713/writing-skills','Opened for context. The invoked science-editor skill was read from the local SKILL.md.')
]:
 body.append(f'<p><a href="{url}">{e(title)}</a>. {e(note)}</p>')
 md.extend([f'- [{title}]({url}). {note}',''])
para('Editorial method: %USERPROFILE%/.agents/skills/science-editor/SKILL.md. Its role description supplies an editorial stance, not a biographical credential of this report’s author.')

heading('Recommended revision sequence','revision')
steps=[
'Repair C01–C06 and their dependent conclusions first. These change what the book teaches. Do not retain a wrong conclusion merely because an earlier page has been shipped.',
'Repair the remaining major definitions, assumptions, statistical interpretations and source readings. Recompute affected tables and figures only after the corrected physical statement is settled.',
'Rewrite introductions, transitions and conclusions module by module in a consistent explanatory voice. Use the 48 edits as examples, not as a substitute for a full prose pass.',
'Reconcile notation, dependencies and missing-scope promises. Remove or relocate production-history paragraphs. Run numerical and rendering checks against the corrected content.',
'Finish with an independent read that asks what is assumed, what follows and what is measured. Reopen evidence whenever a conclusion is stronger than its premises. Perform grammar and punctuation cleanup last.'
]
body.append('<ol>'+''.join('<li>'+e(t)+'</li>' for t in steps)+'</ol>')
md.extend([f'{i+1}. {t}' for i,t in enumerate(steps)]+[''])
heading('What already works','strengths',3)
para('The manuscript should not be discarded. Its worked calculations, explicit source tables, efforts to expose assumptions and several careful distinctions between validation and observation form a substantial foundation. Those virtues are applied inconsistently. The next pass should preserve the useful mathematics, make the conclusions obey it, and give the explanation a stable, direct voice.')
heading('Signature and preservation','signature')
para('Signed: Codex — OpenAI. Independent scientific and prose audit, 20 September 2026, America/Los_Angeles. This signature identifies the author of this report and its proposed wording; it does not attribute these passages to Claude. No original manuscript content was edited.')
body.append('<p class="small"><a href="original-file-hashes.json">Original-file SHA-256 baseline</a> · <a href="integrity-verification.json">Final preservation check</a> · <a href="independent-checks.json">Independent calculations</a> · <a href="findings.json">Structured findings</a> · <a href="AUDIT_REPORT.md">Markdown companion</a></p>')
md.extend(['Evidence: original-file-hashes.json, integrity-verification.json, independent-checks.json, mechanical-checks.json, findings.json and sources/source-manifest.json.',''])

css=r'''
:root{color-scheme:dark;--bg:#10171c;--panel:#19242c;--ink:#edf1f3;--muted:#b4c1ca;--rule:#364650;--accent:#91d8ce;--amber:#edcb91;--red:#ffb4a7}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.72 Georgia,serif}
a{color:var(--accent);text-underline-offset:3px}a:hover{color:white}a:focus-visible,select:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--amber);outline-offset:4px}
.layout{display:grid;grid-template-columns:230px minmax(0,1fr);max-width:1400px;margin:auto}nav{position:sticky;top:0;height:100vh;padding:35px 24px;border-right:1px solid var(--rule);font:13px/1.5 system-ui,sans-serif;overflow:auto}
nav strong{display:block;text-transform:uppercase;font-size:11px;letter-spacing:.1em;color:var(--muted);margin-bottom:28px}nav a{display:block;margin:0 0 14px;text-decoration:none}main{min-width:0;max-width:1070px;padding:45px 60px 80px}
h1{font-size:clamp(34px,4.3vw,54px);font-weight:normal;line-height:1.14;margin:10px 0 28px;letter-spacing:-.02em}h2{font-size:30px;line-height:1.25;font-weight:normal;margin:52px 0 25px;padding-top:35px;border-top:1px solid var(--rule)}
h3{font-size:23px;line-height:1.35;font-weight:normal;margin:28px 0 12px}h4{font:600 12px/1.5 system-ui,sans-serif;text-transform:uppercase;letter-spacing:.07em;color:var(--accent);margin:0 0 15px}p{margin:0 0 19px}
.stats{display:flex;flex-wrap:wrap;gap:25px;margin:30px 0;font:12px system-ui,sans-serif;color:var(--muted)}.stats strong{display:block;font-size:32px;color:var(--accent);font-weight:500;margin-bottom:7px}
.finding,.module-card{border:1px solid var(--rule);background:var(--panel);border-radius:7px;padding:26px;margin:25px 0}.finding h3,.module-card h3{margin-top:13px}.meta,.small{font:12px/1.7 system-ui,sans-serif;color:var(--muted)}
.severity{display:inline-block;text-transform:uppercase;font-size:10px;letter-spacing:.05em;padding:2px 6px;border:1px solid currentColor;border-radius:3px;margin-right:8px}.blocking{color:var(--red)}.major{color:var(--amber)}.moderate{color:var(--accent)}
blockquote{margin:20px 0;padding:5px 0 5px 17px;border-left:3px solid var(--amber);font-style:italic;color:#e7d2af;overflow-wrap:anywhere}.replacement{background:#102026;border-left:3px solid var(--accent);padding:20px;margin:23px 0}.replacement p:last-child{margin-bottom:0}
summary{cursor:pointer;color:var(--accent);font:13px system-ui,sans-serif}pre{white-space:pre-wrap;overflow-wrap:anywhere;padding:17px;background:#0a1115;border:1px solid var(--rule);font:12px/1.6 Consolas,monospace}
.prose-edit{padding:0 0 20px;margin:25px 0;border-bottom:1px solid var(--rule)}.prose-edit p{font-size:16px}.rewrite{padding:14px;background:var(--panel);border-radius:4px}
.filters{display:flex;flex-wrap:wrap;gap:14px;align-items:center;background:var(--panel);padding:14px;border:1px solid var(--rule);border-radius:5px;font:12px system-ui,sans-serif}
select,button{font:13px system-ui,sans-serif;color:var(--ink);background:var(--bg);border:1px solid var(--rule);border-radius:3px;padding:8px}button{cursor:pointer}#count{color:var(--muted)}
.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;font:13px/1.6 system-ui,sans-serif}th,td{padding:12px;text-align:left;border-bottom:1px solid var(--rule)}th{color:var(--accent)}li{margin-bottom:16px}.source{padding-bottom:8px;border-bottom:1px solid var(--rule)}.source h3{font-size:19px}[hidden]{display:none!important}
mjx-container{max-width:100%;overflow-x:auto;overflow-y:hidden;padding:3px 0}
@media(max-width:1000px){.layout{grid-template-columns:190px minmax(0,1fr)}main{padding:35px 30px}nav{padding:28px 18px}}
@media(max-width:700px){.layout{display:block}nav{position:relative;height:auto;display:flex;flex-wrap:wrap;gap:8px 16px;padding:18px 22px;border-right:0;border-bottom:1px solid var(--rule)}nav strong{width:100%;margin:0}nav a{margin:0;font-size:12px}main{padding:30px 20px}.finding,.module-card{padding:19px 16px}h2{font-size:26px}h3{font-size:21px}body{font-size:16px}.stats{gap:20px}}
@media print{:root{--bg:white;--panel:white;--ink:#111;--muted:#444;--rule:#bbb;--accent:#17505a;--amber:#775100;--red:#922819;color-scheme:light}body{font-size:10pt}.layout{display:block}nav,.filters,details{display:none}main{max-width:none;padding:0}.finding[hidden]{display:block!important}.finding,.module-card{break-inside:avoid;border-radius:0;padding:15px}.replacement,.rewrite{background:#f4f4f4}blockquote{color:#333}h1{font-size:30pt}h2{font-size:22pt}h3{font-size:16pt}a{color:#17505a}.stats{font-size:9pt}}
'''
js=r'''
const mf=document.getElementById('module-filter'), sf=document.getElementById('severity-filter');
function filter(){let n=0;document.querySelectorAll('.finding').forEach(x=>{const show=(!mf.value||x.dataset.module===mf.value)&&(!sf.value||x.dataset.severity===sf.value);x.hidden=!show;if(show)n++});document.getElementById('count').textContent=n+' of 40 findings';}
mf.addEventListener('change',filter);sf.addEventListener('change',filter);document.getElementById('reset').addEventListener('click',()=>{mf.value='';sf.value='';filter()});filter();
'''
nav=[('verdict','Verdict'),('scope','Scope & method'),('findings','40 content findings'),('prose','Prose & 48 rewrites'),('modules','All twelve modules'),('structure','Structure & pedagogy'),('production','Production checks'),('sources','Evidence & sources'),('revision','Revision sequence'),('signature','Signature')]
doc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="Codex — OpenAI"><title>Textbook audit — Codex — 20 September 2026</title><style>'+css+'</style><script>window.MathJax={tex:{inlineMath:[["$","$"]],displayMath:[["$$","$$"]]},options:{skipHtmlTags:["script","noscript","style","textarea","pre","code"]},svg:{fontCache:"global"}};</script><script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-svg.js"></script></head><body><div class="layout"><nav aria-label="Report sections"><strong>Codex / Independent audit</strong>'+''.join(f'<a href="#{i}">{label}</a>' for i,label in nav)+'</nav><main>'+''.join(body)+'</main></div><script>'+js+'</script></body></html>'
(OUT/'AUDIT_REPORT.html').write_text(doc,encoding='utf8')
(OUT/'AUDIT_REPORT.md').write_text('\n'.join(md),encoding='utf8')
manifest=json.loads((OUT/'sources/source-manifest.json').read_text(encoding='utf8'))
for s in manifest:
 s['status']='downloaded; relevant passages inspected; not a full-paper audit'
 s['inspected_pdf_pages']={'marrone2007':[4],'zhuravleva2019':[1,4,5,12],'kandori2005':[4,5],'troland2008':[2,3],'king2007':[4,6],'venzheimer2018':[8]}[s['id']]
(OUT/'sources/source-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print(json.dumps({'content':len(F),'prose':len(P),'html_bytes':len(doc.encode()),'markdown_words':len(' '.join(md).split()),'approx_manuscript_tokens':sum(x['words'] for x in inv)},indent=2))
