# Codex textbook audit rubric

This rubric governs the independent scientific and editorial audit of the *Astrophysical Fluid Dynamics* modules. It combines the twenty-rule prose standard with checks for scientific correctness, evidence, derivations, pedagogy, notation, and production quality.

The audit must not modify existing module files. Findings, evidence, proposed replacements, and any later rewritten edition belong inside the `codex-audit-2026-09-20` folder.

## A. Twenty-rule prose standard

1. Write in clear, natural academic English suitable for advanced undergraduate or beginning graduate readers.
2. Give each paragraph one identifiable idea. State it, explain it, and identify its physical consequence.
3. Prefer sentences of 15–25 words. Split sentences longer than about 35 words unless their structure is exceptionally clear.
4. Do not combine independent claims using comma chains, semicolons, parentheses, or repeated dashes.
5. Remove synthetic rhetoric, dramatic verdicts, slogans, fake suspense, and self-conscious commentary.
6. Avoid personification such as “the answer lives here,” “the theory pays a debt,” or “the premise is spent.”
7. Keep the writing and production process out of the textbook narrative.
8. Separate physical exposition from source criticism and editorial provenance.
9. Define every symbol before use and state assumptions before drawing conclusions.
10. Distinguish derivations, approximations, empirical comparisons, interpretations, and conjectures.
11. Use cautious language only for a specific, identifiable uncertainty.
12. Place each qualification immediately beside the claim it restricts.
13. Remove repetitive announcements such as “this is the result” or “this is the point.”
14. Avoid casual claims that evidence “confirms” or “refutes” a theory. Present the comparison and justified inference.
15. Base transitions on the scientific argument rather than the module-production process.
16. Keep paragraphs reasonably short without creating choppy sequences of one-sentence paragraphs.
17. Apply a read-aloud test and rewrite prose that sounds bureaucratic, mechanical, theatrical, or unnatural.
18. Check adjacent modules for consistent terminology, notation, assumptions, and scientific conclusions.
19. Retain an existing sentence only if it already meets the textbook standard, not merely because it is grammatical.
20. Do not modify the existing module files. Any revised edition must be placed in a separate folder.

## B. Scientific claim standard

Every substantive claim must satisfy five requirements:

1. **Precise statement.** State exactly what is claimed and under which conditions.
2. **Defined terms.** Define every variable, technical term, convention, and reference frame before use.
3. **Visible mechanism.** Derive the result in the smallest setting that reveals why it is true.
4. **Limits and rescue cases.** State where the result fails and what added physics modifies or restores it.
5. **Concrete connection.** Connect the claim to a calculation, observation, simulation, figure, or primary source.

The audit also checks algebra, calculus, signs, factors, units, dimensions, substitutions, initial and boundary conditions, constitutive assumptions, closure relations, limiting cases, internal consistency, inequality directions, statistics, and consistency among equations, prose, tables, figures, captions, examples, exercises, and conclusions.

## C. Sources and evidence

- Read the primary source behind each important citation and verify the cited passage.
- Check numerical values against the source’s definitions, tables, and units.
- Distinguish measurements, model outputs, fitted parameters, reconstructed quantities, and assumptions.
- Flag citations that support only a weaker claim or cannot be verified.
- Do not repair citations from memory.
- Check whether the module’s calculations or later evidence contradict its interpretation.
- Preserve a source map connecting major findings to their evidence.

## D. Derivations, calculations, and exercises

- Reproduce important derivations independently and inspect intermediate steps.
- Test dimensions, signs, simple limits, and selected numerical examples.
- Check whether displayed numerical precision is justified.
- Confirm that exercises are solvable from the preceding text and verify worked solutions where supplied.
- Distinguish a code implementation check from independent scientific validation.

## E. Pedagogy and structure

- Open with a clear physical question and motivate concepts before formalism.
- Supply a nearby worked example for each major new concept.
- Keep dependencies backward-pointing or prove required material in place.
- Move coherently from assumptions through derivation to interpretation.
- Use scientifically motivated transitions.
- Close by stating what the reader can now calculate or understand.
- Arrange exercises in increasing difficulty and make them self-contained.
- Require every figure to add information and every caption to stand alone.
- Judge whether a quantitatively trained reader new to the subfield can learn from the module without hidden prerequisites.

## F. Notation and cross-module consistency

- Introduce each symbol before use and keep its meaning stable.
- Follow standard field conventions unless alternatives are explained.
- Distinguish vectors, tensors, scalars, averages, perturbations, and dimensionless quantities.
- Keep indices, subscripts, signs, coordinates, and normalizations consistent.
- Verify cross-references and prerequisite claims against adjacent modules.
- Flag silent reversals or overstatements of conclusions established elsewhere.

## G. Figures, tables, HTML, and production quality

- Validate HTML and MathJax delimiters.
- Detect malformed equations, duplicate anchors, and broken internal links.
- Preserve figures, tables, scripts, navigation, and accessibility text.
- Check figure labels, units, legends, captions, and table definitions.
- Check desktop and mobile rendering for overflow and JavaScript errors.
- Record original module hashes before the audit and verify them afterward.

## H. Required audit deliverable

The signed report must contain:

1. A module-level verdict: **acceptable**, **acceptable after revision**, or **not yet teachable**.
2. Findings ranked as **blocking**, **major**, or **minor**.
3. Exact `file:line` locations and quoted source text.
4. The violated rubric item and an explanation of the defect.
5. Full proposed replacement text rather than vague editing instructions.
6. Representative prose rewrites.
7. Structural and pedagogical recommendations.
8. Independent numerical checks.
9. A primary-source evidence map.
10. Specific passages that already work and should be retained.
11. A preservation record showing that original modules were not changed.
12. A Codex signature distinguishing this audit from the original Claude-authored material.

Signed: **Codex — OpenAI**  
Rubric recorded: 22 September 2026, America/Los_Angeles
