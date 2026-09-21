"""Validate the twelve revised copies and prove that their sources are unchanged."""
from __future__ import annotations
from pathlib import Path
from urllib.parse import unquote
from bs4 import BeautifulSoup
import hashlib
import json

AUDIT = Path(__file__).resolve().parent
ROOT = AUDIT.parent
DEST = AUDIT / "revised-modules"

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = json.loads((DEST / "build-manifest.json").read_text(encoding="utf-8"))
assert len(manifest["modules"]) == 12
content_ids = [item for record in manifest["modules"] for item in record["content_findings_applied"]]
prose_ids = [
    item for record in manifest["modules"]
    for key in ("prose_edits_applied_before_content_replacements", "prose_edits_not_found_or_superseded")
    for item in record[key]
]
assert len(content_ids) == len(set(content_ids)) == 40
assert len(prose_ids) == len(set(prose_ids)) == 48

errors: list[str] = []
for record in manifest["modules"]:
    source = ROOT / record["source"]
    revised = ROOT / record["destination"]
    if digest(source) != record["source_sha256"]:
        errors.append(f"source changed after build: {source}")
    if digest(revised) != record["revised_sha256"]:
        errors.append(f"revised hash mismatch: {revised}")
    soup = BeautifulSoup(revised.read_text(encoding="utf-8"), "html.parser")
    if not soup.select_one(".codex-revision"):
        errors.append(f"missing revision notice: {revised.name}")
    ids = {tag.get("id") for tag in soup.find_all(id=True)}
    for a in soup.find_all("a", href=True):
        href = unquote(a["href"])
        if href.startswith(("http:", "https:", "mailto:")):
            continue
        path, _, fragment = href.partition("#")
        target = (revised.parent / (path or revised.name)).resolve()
        if not target.exists():
            errors.append(f"dead link in {revised.name}: {href}")
            continue
        if fragment:
            target_ids = ids if target == revised else {
                tag.get("id") for tag in BeautifulSoup(target.read_text(encoding="utf-8"), "html.parser").find_all(id=True)
            }
            if fragment not in target_ids:
                errors.append(f"dead fragment in {revised.name}: {href}")

for required in ("index.html", "README.md", "build-manifest.json"):
    if not (DEST / required).exists():
        errors.append(f"missing edition file: {required}")

if errors:
    raise SystemExit("\n".join(errors))
print("PASS: 12 revised modules; 40 content findings; 48 prose findings; source hashes unchanged; local links valid")
