from __future__ import annotations

import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


baseline = json.loads((HERE / "original-module-hashes.json").read_text(encoding="utf-8"))
checks = []
for rel, recorded in baseline["files"].items():
    current = ROOT / rel
    actual = sha256(current)
    checks.append({"file": rel, "baseline_sha256": recorded["sha256"], "current_sha256": actual, "unchanged": actual == recorded["sha256"]})

integrity = {
    "baseline_commit": baseline["recorded_at_commit"],
    "module_count": len(checks),
    "all_original_modules_unchanged": all(row["unchanged"] for row in checks),
    "files": checks,
}
(HERE / "integrity-verification.json").write_text(json.dumps(integrity, indent=2) + "\n", encoding="utf-8")


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])


html_path = HERE / "AUDIT_REPORT.html"
text = html_path.read_text(encoding="utf-8")
parser = Parser()
parser.feed(text)
finding_ids = [row["id"] for row in json.loads((HERE / "findings.json").read_text(encoding="utf-8"))]
validation = {
    "html_bytes": html_path.stat().st_size,
    "parser_errors": 0,
    "duplicate_ids": sorted({x for x in parser.ids if parser.ids.count(x) > 1}),
    "has_signature": "Codex — OpenAI" in text,
    "has_all_finding_ids": all(x in text for x in finding_ids),
    "has_twenty_rules": all(f"> {n} <" in text or f">{n}<" in text for n in range(1, 21)),
    "external_links": sum(link.startswith(("http://", "https://")) for link in parser.links),
}
(HERE / "report-validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")

artifact_hashes = {
    path.name: sha256(path)
    for path in sorted(HERE.iterdir())
    if path.is_file() and path.name != "artifact-sha256.json"
}
(HERE / "artifact-sha256.json").write_text(json.dumps(artifact_hashes, indent=2) + "\n", encoding="utf-8")

assert integrity["all_original_modules_unchanged"]
assert not validation["duplicate_ids"]
assert validation["has_signature"] and validation["has_all_finding_ids"] and validation["has_twenty_rules"]
print(json.dumps({"integrity": integrity["all_original_modules_unchanged"], "report": validation}, indent=2))
