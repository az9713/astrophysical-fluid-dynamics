"""Mechanical checks supporting the twenty-rule editorial review.

These checks do not certify paragraph unity, scientific judgement, or natural
cadence. Those requirements remain manual editorial gates in REWRITE_STATUS.md.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import json
import re

ROOT = Path(__file__).resolve().parent
DEST = ROOT / "textbook-edition-20-rule"
BASELINE = ROOT / "revised-modules"

BANNED = re.compile(
    r"paper was read|was read for this book|project has no source|"
    r"first draft|shipped module|Gate D|the answer lives|premise is spent|"
    r"this module exists to|pays? (?:its|the) debt|hold that number|"
    r"the generator (?:returns|produced|broke)|repayment is this paragraph",
    re.I,
)
ANNOUNCEMENTS = re.compile(
    r"\bthis is (?:the point|the result|what the figure shows)\b", re.I
)
SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Z“"$<])')

errors = []
report = {"modules": []}

for number in range(1, 13):
    path = DEST / f"module{number:02}.html"
    baseline = BASELINE / path.name
    if not path.is_file():
        errors.append(f"missing {path.name}")
        continue
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    base_soup = BeautifulSoup(baseline.read_text(encoding="utf-8"), "html.parser")
    for required in ("html", "head", "body", "title"):
        if soup.find(required) is None:
            errors.append(f"{path.name}: missing <{required}>")
    old_ids = {x["id"] for x in base_soup.find_all(id=True)}
    new_ids = {x["id"] for x in soup.find_all(id=True)}
    missing_ids = sorted(old_ids - new_ids)
    if missing_ids:
        errors.append(f"{path.name}: lost anchors {missing_ids}")
    old_figures = [x.get("src") for x in base_soup.find_all("img")]
    new_figures = [x.get("src") for x in soup.find_all("img")]
    if old_figures != new_figures:
        errors.append(f"{path.name}: figure source list changed")

    long_sentences = []
    banned_hits = []
    blocks = 0
    for tag in soup.find_all(["p", "li", "figcaption"]):
        if tag.find_parent("nav") or tag.find_parent("header"):
            continue
        text = tag.get_text(" ", strip=True)
        if not text:
            continue
        blocks += 1
        if BANNED.search(text) or ANNOUNCEMENTS.search(text):
            banned_hits.append(text[:180])
        for sentence in SENTENCE_SPLIT.split(text):
            words = len(sentence.split())
            # Displays often appear between two prose sentences in one HTML block.
            # They are reported only above 50 words and must still be reviewed.
            limit = 50 if "$$" in sentence else 35
            if words > limit:
                long_sentences.append({"words": words, "text": sentence[:240]})
    if banned_hits:
        errors.extend(f"{path.name}: banned rhetoric: {hit}" for hit in banned_hits)
    report["modules"].append(
        {
            "module": number,
            "prose_blocks": blocks,
            "long_sentence_flags": long_sentences,
            "banned_rhetoric_hits": len(banned_hits),
            "missing_anchor_count": len(missing_ids),
        }
    )

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = href.split("#", 1)[0]
        if target and not (DEST / target).exists():
            errors.append(f"{path.name}: broken local link {href}")

(DEST / "validation-20-rule.json").write_text(
    json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
)

if errors:
    raise SystemExit("\n".join(errors))

flag_total = sum(len(m["long_sentence_flags"]) for m in report["modules"])
print(f"STRUCTURAL PASS: 12 modules; {flag_total} sentences require editorial review")
