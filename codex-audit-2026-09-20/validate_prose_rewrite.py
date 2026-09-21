"""Regression gates for the human-written textbook prose pass."""
from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT = Path(__file__).resolve().parent
DEST = ROOT / "revised-modules"
production = re.compile(
    r"paper was read|was read for this book|project has no source|"
    r"first draft|shipped module|Gate D|the answer lives|premise is spent|"
    r"this module exists to|pays? (?:its|the) debt",
    re.I,
)
errors: list[str] = []

for path in sorted(DEST.glob("module*.html")):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    in_back_matter = False
    for tag in soup.find_all(["h2", "p", "li", "figcaption"]):
        if tag.name == "h2" and tag.get("id") in {"problems", "notation", "sources"}:
            in_back_matter = True
        text = tag.get_text(" ", strip=True)
        if not in_back_matter and production.search(text):
            errors.append(f"production narration in {path.name}: {text[:120]}")
        if in_back_matter:
            continue
        for sentence in re.split(r'(?<=[.!?])\s+(?=[A-Z“"<])', text):
            words = len(sentence.split())
            # Display equations and exact quotations are reviewed separately;
            # the numerical word count is not meaningful for either.
            if words > 50 and "$$" not in sentence and sentence.count('"') < 2:
                errors.append(f"overloaded sentence ({words} words) in {path.name}: {sentence[:120]}")

whole = "\n".join(p.read_text(encoding="utf-8") for p in DEST.glob("module*.html"))
for banned in (
    "Row by row:",
    "has no source in this project",
    "the paper was read",
    "the generator broke",
    "the repayment is this paragraph",
):
    if banned.lower() in whole.lower():
        errors.append(f"banned manuscript-production phrase remains: {banned}")

if errors:
    raise SystemExit("\n".join(errors))
print("PASS: prose gates satisfied in all 12 teaching narratives")
