"""Final structural, editorial, and preservation checks for the 20-rule edition."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from pathlib import Path
import json
import re

from bs4 import BeautifulSoup, Tag


ROOT = Path(__file__).resolve().parent
BASE = ROOT / "revised-modules"
DEST = ROOT / "textbook-edition-20-rule"
REPO = ROOT.parent

SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z“"$<])')
WORD = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?")
DISPLAY = re.compile(r"\$\$(.*?)\$\$", re.S)
MATH = re.compile(r"\$\$.*?\$\$|\$.*?\$", re.S)
PRODUCTION = re.compile(
    r"first draft|shipped (?:page|module)|the generator|build session|"
    r"production code|web summariser|this project has no source|"
    r"the paper was read|was read for this book|Gate D",
    re.I,
)
SYNTHETIC = re.compile(
    r"\bdebt\b|\brepay(?:s|ment|ing)?\b|\brepaid\b|the answer lives|"
    r"hold that number|premise is spent|pays? (?:its|the) debt|"
    r"theory pays|calculation refutes itself|whole of it|will not pretend",
    re.I,
)
VERDICT = re.compile(r"\bconfirmed\b|\brefuted\b|\brefutation\b|\bverdict\b", re.I)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def text_before_sources(soup: BeautifulSoup) -> str:
    source = soup.find(id="sources")
    chunks = []
    for tag in soup.find_all(["p", "li", "figcaption", "div", "span", "td", "text"]):
        if source and source in tag.find_all_previous():
            continue
        if tag.name in {"div", "span", "td"} and tag.find(
            ["p", "li", "figcaption", "div", "span", "td"]
        ):
            continue
        if tag.find_parent(["pre", "code", "script", "style"]) or tag.find(
            ["pre", "code", "script", "style"]
        ):
            continue
        value = " ".join(tag.get_text(" ", strip=True).split())
        if value:
            chunks.append(value)
    return "\n".join(chunks)


def prose_sentences(soup: BeautifulSoup):
    source = soup.find(id="sources")
    for tag in soup.find_all(["p", "li", "figcaption", "div", "span", "td"]):
        if source and source in tag.find_all_previous():
            continue
        if tag.name in {"div", "span", "td"} and tag.find(
            ["p", "li", "figcaption", "div", "span", "td"]
        ):
            continue
        if tag.find_parent(["pre", "code", "script", "style"]) or tag.find(
            ["pre", "code", "script", "style"]
        ):
            continue
        text = " ".join(tag.get_text(" ", strip=True).split())
        text = MATH.sub(" EQUATION ", text)
        for sentence in SENTENCE_SPLIT.split(text):
            words = WORD.findall(sentence)
            if words:
                yield len(words), sentence


def table_shape(soup: BeautifulSoup):
    return [
        [len(row.find_all(["td", "th"], recursive=False)) for row in table.find_all("tr")]
        for table in soup.find_all("table")
    ]


errors: list[str] = []
report = {"edition": "20-rule textbook prose edition", "modules": []}
target_id_cache: dict[Path, set[str]] = {}

original_hashes = json.loads((ROOT / "original-file-hashes.json").read_text(encoding="utf-8"))
build = json.loads((ROOT / "revised-modules" / "build-manifest.json").read_text(encoding="utf-8"))
revised_hashes = {Path(m["destination"]).name: m["revised_sha256"] for m in build["modules"]}

for number in range(1, 13):
    name = f"module{number:02d}.html"
    base_path = BASE / name
    path = DEST / name
    original_path = REPO / "afd" / name
    raw = path.read_text(encoding="utf-8")
    base_raw = base_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    base_soup = BeautifulSoup(base_raw, "html.parser")

    for required in ("html", "head", "body", "title"):
        if soup.find(required) is None:
            errors.append(f"{name}: missing <{required}>")

    ids = [tag["id"] for tag in soup.find_all(id=True)]
    base_ids = [tag["id"] for tag in base_soup.find_all(id=True)]
    duplicate_ids = sorted(key for key, value in Counter(ids).items() if value > 1)
    if set(ids) != set(base_ids):
        errors.append(f"{name}: anchor set changed")
    if duplicate_ids:
        errors.append(f"{name}: duplicate ids {duplicate_ids}")

    displays = [m.group(0) for m in DISPLAY.finditer(raw)]
    base_displays = [m.group(0) for m in DISPLAY.finditer(base_raw)]
    if displays != base_displays:
        errors.append(f"{name}: displayed mathematics changed")

    scripts = [str(tag) for tag in soup.find_all("script")]
    base_scripts = [str(tag) for tag in base_soup.find_all("script")]
    styles = [str(tag) for tag in soup.find_all("style")]
    base_styles = [str(tag) for tag in base_soup.find_all("style")]
    if scripts != base_scripts:
        errors.append(f"{name}: scripts changed")
    if styles != base_styles:
        errors.append(f"{name}: styles changed")

    image_sources = [tag.get("src") for tag in soup.find_all("img")]
    base_image_sources = [tag.get("src") for tag in base_soup.find_all("img")]
    if image_sources != base_image_sources:
        errors.append(f"{name}: image sources changed")
    if len(soup.find_all("svg")) != len(base_soup.find_all("svg")):
        errors.append(f"{name}: inline SVG count changed")
    if table_shape(soup) != table_shape(base_soup):
        errors.append(f"{name}: table row/cell structure changed")

    for tag_name in ("div", "span", "p", "table", "tr", "td"):
        opens = len(re.findall(fr"<{tag_name}\b", raw, re.I))
        closes = len(re.findall(fr"</{tag_name}>", raw, re.I))
        if opens != closes:
            errors.append(f"{name}: unbalanced <{tag_name}> ({opens}/{closes})")

    broken_links = []
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith(("http://", "https://", "mailto:")):
            continue
        file_part, _, anchor = href.partition("#")
        target_path = DEST / file_part if file_part else path
        if not target_path.exists():
            broken_links.append(href)
            continue
        if anchor:
            if target_path not in target_id_cache:
                target_soup = BeautifulSoup(
                    target_path.read_text(encoding="utf-8"), "html.parser"
                )
                target_id_cache[target_path] = {
                    node["id"] for node in target_soup.find_all(id=True)
                }
            if anchor not in target_id_cache[target_path]:
                broken_links.append(href)
    if broken_links:
        errors.append(f"{name}: broken local links {sorted(set(broken_links))}")

    body_text = text_before_sources(soup)
    production_hits = PRODUCTION.findall(body_text)
    synthetic_hits = SYNTHETIC.findall(body_text)
    verdict_hits = VERDICT.findall(body_text)
    if production_hits:
        errors.append(f"{name}: production narration remains {production_hits}")
    if synthetic_hits:
        errors.append(f"{name}: synthetic rhetoric remains {synthetic_hits}")
    if verdict_hits:
        errors.append(f"{name}: verdict rhetoric remains {verdict_hits}")
    if "\ufffd" in raw or any(ord(ch) < 32 and ch not in "\n\r\t" for ch in raw):
        errors.append(f"{name}: damaged or control characters")

    sentence_lengths = [count for count, _ in prose_sentences(soup)]
    over_50 = [count for count in sentence_lengths if count > 50]
    review_36_50 = [count for count in sentence_lengths if 36 <= count <= 50]
    preferred = [count for count in sentence_lengths if 15 <= count <= 25]
    if over_50:
        errors.append(f"{name}: sentences longer than 50 words {over_50}")

    original_expected = original_hashes[f"afd/{name}"]
    original_unchanged = digest(original_path) == original_expected
    revised_unchanged = digest(base_path) == revised_hashes[name]
    if not original_unchanged:
        errors.append(f"{name}: original afd file hash changed")
    if not revised_unchanged:
        errors.append(f"{name}: revised baseline file hash changed")

    report["modules"].append(
        {
            "module": number,
            "sha256": digest(path),
            "anchors_preserved": set(ids) == set(base_ids),
            "displayed_mathematics_exact": displays == base_displays,
            "scripts_exact": scripts == base_scripts,
            "styles_exact": styles == base_styles,
            "figures_preserved": image_sources == base_image_sources
            and len(soup.find_all("svg")) == len(base_soup.find_all("svg")),
            "table_structure_preserved": table_shape(soup) == table_shape(base_soup),
            "broken_local_links": sorted(set(broken_links)),
            "sentence_count": len(sentence_lengths),
            "sentences_15_to_25": len(preferred),
            "sentences_36_to_50_reviewed": len(review_36_50),
            "sentences_over_50": len(over_50),
            "production_narration_hits": len(production_hits),
            "synthetic_rhetoric_hits": len(synthetic_hits),
            "verdict_rhetoric_hits": len(verdict_hits),
            "original_afd_unchanged": original_unchanged,
            "revised_baseline_unchanged": revised_unchanged,
        }
    )

report["summary"] = {
    "module_count": len(report["modules"]),
    "all_checks_pass": not errors,
    "total_sentences": sum(m["sentence_count"] for m in report["modules"]),
    "total_sentences_15_to_25": sum(m["sentences_15_to_25"] for m in report["modules"]),
    "total_sentences_36_to_50_reviewed": sum(
        m["sentences_36_to_50_reviewed"] for m in report["modules"]
    ),
    "total_sentences_over_50": sum(m["sentences_over_50"] for m in report["modules"]),
    "errors": errors,
}

(DEST / "certification-report.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
)

if errors:
    raise SystemExit("\n".join(errors))
print(
    "CERTIFICATION PASS: 12 modules; exact displayed mathematics; preserved anchors, "
    "scripts, figures, tables, and baselines; no unresolved >50-word sentences"
)
