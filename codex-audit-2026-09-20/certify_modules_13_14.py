"""Check the separate 20-rule editions of Modules 13 and 14."""

from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import re

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
EDITION = ROOT / "textbook-edition-20-rule"
BASELINE = json.loads(
    (ROOT / "delta-audit-2026-09-22" / "original-module-hashes.json").read_text(
        encoding="utf-8"
    )
)["files"]
DISPLAY = re.compile(r"\$\$(.*?)\$\$", re.S)
MATH = re.compile(r"\$\$.*?\$\$|\$.*?\$", re.S)
SENTENCE = re.compile(r'(?<=[.!?])\s+(?=[A-Z“"$<])')
WORD = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?")
PRODUCTION = re.compile(
    r"\bdebt\b|\bshipped\b|\bconfirmed\b|\brefuted\b|"
    r"first draft|the generator|the plan of this book|Gate D|pays? the debt|"
    r"refused in print",
    re.I,
)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def table_shape(soup):
    return [
        [len(row.find_all(["td", "th"], recursive=False)) for row in table.find_all("tr")]
        for table in soup.find_all("table")
    ]


def teaching_text(soup):
    pieces = []
    for node in soup.body.children:
        if getattr(node, "get", lambda _: None)("id") == "sources":
            break
        if getattr(node, "name", None) in {"script", "style", "nav", "aside"}:
            continue
        if hasattr(node, "get_text"):
            pieces.append(node.get_text(" ", strip=True))
    return " ".join(pieces)


def sentence_lengths(soup):
    source = soup.find(id="sources")
    for tag in soup.find_all(["p", "li", "figcaption", "div", "span", "td"]):
        if source and source in tag.find_all_previous():
            continue
        if tag.name in {"div", "span", "td"} and tag.find(
            ["p", "li", "figcaption", "div", "span", "td"]
        ):
            continue
        if tag.find_parent(["pre", "code", "script", "style", "aside"]):
            continue
        if tag.find(["pre", "code", "script", "style"]):
            continue
        prose = MATH.sub(" EQUATION ", " ".join(tag.get_text(" ", strip=True).split()))
        for sentence in SENTENCE.split(prose):
            words = WORD.findall(sentence)
            if words:
                yield len(words), sentence


errors = []
report = {"edition": "Codex 20-rule edition, Modules 13–14", "modules": []}
for module in (13, 14):
    name = f"module{module:02}.html"
    original = REPO / "afd" / name
    revised = EDITION / name
    original_raw = original.read_text(encoding="utf-8")
    revised_raw = revised.read_text(encoding="utf-8")
    old = BeautifulSoup(original_raw, "html.parser")
    new = BeautifulSoup(revised_raw, "html.parser")
    entry = {"module": module, "original_sha256": digest(original), "codex_sha256": digest(revised)}
    if entry["original_sha256"] != BASELINE[f"afd/{name}"]["sha256"]:
        errors.append(f"{name}: original differs from audit baseline")
    old_ids = [node["id"] for node in old.find_all(id=True)]
    new_ids = [node["id"] for node in new.find_all(id=True)]
    if set(old_ids) != set(new_ids) or len(new_ids) != len(set(new_ids)):
        errors.append(f"{name}: anchor set changed or duplicate anchor")
    if DISPLAY.findall(original_raw) != DISPLAY.findall(revised_raw):
        errors.append(f"{name}: displayed mathematics changed")
    for tag in ("script", "style", "figure", "svg"):
        before = old.find_all(tag)
        after = new.find_all(tag)
        if tag in {"script", "style"}:
            if [str(t) for t in before] != [str(t) for t in after]:
                errors.append(f"{name}: {tag} content changed")
        elif len(before) != len(after):
            errors.append(f"{name}: {tag} count changed")
    if [str(tag) for tag in old.find_all("svg")] != [
        str(tag) for tag in new.find_all("svg")
    ]:
        errors.append(f"{name}: embedded SVG content changed")
    if [tag.get("src") for tag in old.find_all("img")] != [
        tag.get("src") for tag in new.find_all("img")
    ]:
        errors.append(f"{name}: image sources changed")
    if table_shape(old) != table_shape(new):
        errors.append(f"{name}: table row or cell structure changed")
    for tag in ("div", "p", "table", "tr", "td", "figure"):
        opening = len(re.findall(fr"<{tag}\b", revised_raw, re.I))
        closing = len(re.findall(fr"</{tag}>", revised_raw, re.I))
        if opening != closing:
            errors.append(f"{name}: unbalanced {tag} ({opening}/{closing})")
    broken = []
    for link in new.find_all("a", href=True):
        href = link["href"]
        if href.startswith(("https://", "http://", "mailto:")):
            continue
        file_part, _, fragment = href.partition("#")
        target = (revised.parent / file_part).resolve() if file_part else revised
        if not target.exists():
            broken.append(href)
        elif fragment:
            target_soup = BeautifulSoup(target.read_text(encoding="utf-8"), "html.parser")
            if target_soup.find(id=fragment) is None:
                broken.append(href)
    if broken:
        errors.append(f"{name}: broken local links: {sorted(set(broken))}")
    prose = MATH.sub(" EQUATION ", teaching_text(new))
    production = PRODUCTION.findall(prose)
    if production:
        errors.append(f"{name}: production/verdict words remain: {production}")
    lengths = [length for length, _ in sentence_lengths(new)]
    over50 = [length for length in lengths if length > 50]
    if over50:
        errors.append(f"{name}: sentences over 50 words: {over50[:12]}")
    if "\ufffd" in revised_raw:
        errors.append(f"{name}: replacement character remains")
    entry.update(
        {
            "anchors_preserved": set(old_ids) == set(new_ids),
            "displayed_mathematics_exact": DISPLAY.findall(original_raw) == DISPLAY.findall(revised_raw),
            "figures": len(new.find_all("figure")),
            "tables": len(new.find_all("table")),
            "sentences_over_50": len(over50),
            "broken_local_links": sorted(set(broken)),
            "production_or_verdict_hits": production,
        }
    )
    report["modules"].append(entry)

index = BeautifulSoup((EDITION / "index.html").read_text(encoding="utf-8"), "html.parser")
index_links = index.select("ol a[href]")
if len(index_links) != 14:
    errors.append(f"index.html: expected 14 module links, got {len(index_links)}")
for link in index_links:
    if not (EDITION / link["href"]).exists():
        errors.append(f"index.html: missing {link['href']}")

report["all_checks_pass"] = not errors
report["errors"] = errors
(EDITION / "certification-13-14.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
)
if errors:
    raise SystemExit("\n".join(errors))
print("PASS: Modules 13–14; originals, mathematics, figures, tables, anchors, and links intact")
