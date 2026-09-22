from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[2]
AFD = ROOT / "afd"
OUT = Path(__file__).resolve().parent

BLOCK_TAGS = ("h1", "h2", "h3", "h4", "p", "li", "figcaption", "tr")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9$\"'‘“(])")
WORD_RE = re.compile(r"\b[\w’'-]+\b")

PHRASES = {
    "synthetic_rhetoric": [
        "the answer lives here",
        "the theory pays",
        "hold that number",
        "the premise is spent",
        "this module exists to",
        "the calculation refutes itself",
        "this is the point",
        "this is the result",
    ],
    "production_narration": [
        "the paper was read",
        "this project has no source",
        "the generator",
        "the preparation run",
        "the first draft",
        "a shipped module",
        "gate d",
        "source ledger",
    ],
    "evidence_verdicts": ["confirmed", "refuted"],
    "claim_classification": ["measured", "observed", "simulation", "model output"],
    "hedging_or_hype": [
        "obviously",
        "clearly",
        "it is easy to see",
        "simply",
        "powerful",
        "revolutionary",
        "elegant",
    ],
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cleaned_soup(path: Path) -> BeautifulSoup:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for tag in soup(["script", "style", "svg", "nav"]):
        tag.decompose()
    return soup


def block_rows(path: Path) -> list[dict[str, object]]:
    soup = cleaned_soup(path)
    rows: list[dict[str, object]] = []
    for tag in soup.find_all(BLOCK_TAGS):
        if tag.find_parent(BLOCK_TAGS):
            continue
        text = " ".join(tag.get_text(" ", strip=True).split())
        if not text:
            continue
        rows.append({"line": tag.sourceline, "tag": tag.name, "text": text})
    return rows


def sentence_rows(module: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    for row in rows:
        if row["tag"] not in {"p", "li", "figcaption"}:
            continue
        for sentence in SENTENCE_RE.split(str(row["text"])):
            words = WORD_RE.findall(sentence)
            if len(words) > 35:
                found.append(
                    {
                        "module": module,
                        "line": row["line"],
                        "words": len(words),
                        "sentence": sentence,
                    }
                )
    return found


def sentence_stats(rows: list[dict[str, object]]) -> dict[str, int]:
    bins = {"total": 0, "0_to_14": 0, "15_to_25": 0, "26_to_35": 0, "36_to_50": 0, "over_50": 0}
    for row in rows:
        if row["tag"] not in {"p", "li", "figcaption"}:
            continue
        for sentence in SENTENCE_RE.split(str(row["text"])):
            count = len(WORD_RE.findall(sentence))
            if count == 0:
                continue
            bins["total"] += 1
            if count <= 14:
                bins["0_to_14"] += 1
            elif count <= 25:
                bins["15_to_25"] += 1
            elif count <= 35:
                bins["26_to_35"] += 1
            elif count <= 50:
                bins["36_to_50"] += 1
            else:
                bins["over_50"] += 1
    return bins


def phrase_rows(module: str, rows: list[dict[str, object]]) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    for row in rows:
        lowered = str(row["text"]).lower()
        for category, phrases in PHRASES.items():
            for phrase in phrases:
                if phrase in lowered:
                    found.append(
                        {
                            "module": module,
                            "line": row["line"],
                            "category": category,
                            "phrase": phrase,
                            "text": row["text"],
                        }
                    )
    return found


def link_checks(paths: list[Path]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    ids: dict[str, set[str]] = {}
    duplicate_ids: list[dict[str, object]] = []
    soups: dict[str, BeautifulSoup] = {}
    for path in paths:
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        soups[path.name] = soup
        seen: set[str] = set()
        for tag in soup.find_all(id=True):
            anchor = str(tag.get("id"))
            if anchor in seen:
                duplicate_ids.append({"file": path.name, "id": anchor, "line": tag.sourceline})
            seen.add(anchor)
        ids[path.name] = seen

    broken: list[dict[str, object]] = []
    for source_name, soup in soups.items():
        for tag in soup.find_all("a", href=True):
            href = str(tag.get("href"))
            if href.startswith(("http://", "https://", "mailto:", "javascript:")):
                continue
            if href.startswith("#"):
                target_file = source_name
                target_id = href[1:]
            else:
                parts = href.split("#", 1)
                target_file = parts[0]
                target_id = parts[1] if len(parts) == 2 else ""
            if not target_file.endswith(".html"):
                continue
            if target_file not in ids:
                broken.append(
                    {"source": source_name, "line": tag.sourceline, "href": href, "reason": "missing file"}
                )
            elif target_id and target_id not in ids[target_file]:
                broken.append(
                    {"source": source_name, "line": tag.sourceline, "href": href, "reason": "missing anchor"}
                )
    return duplicate_ids, broken


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    module_paths = sorted(AFD.glob("module*.html"))
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    hashes = {
        "recorded_at_commit": commit,
        "files": {
            str(path.relative_to(ROOT)).replace("\\", "/"): {
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
                "lines": len(path.read_text(encoding="utf-8").splitlines()),
            }
            for path in module_paths
        },
    }
    (OUT / "original-module-hashes.json").write_text(
        json.dumps(hashes, indent=2) + "\n", encoding="utf-8"
    )

    all_long: list[dict[str, object]] = []
    all_phrases: list[dict[str, object]] = []
    stats_by_module: dict[str, dict[str, int]] = {}
    for path in module_paths:
        rows = block_rows(path)
        all_long.extend(sentence_rows(path.name, rows))
        all_phrases.extend(phrase_rows(path.name, rows))
        stats_by_module[path.name] = sentence_stats(rows)
        if path.stem in {"module13", "module14"}:
            rendered = [f"{row['line']} [{row['tag']}]: {row['text']}" for row in rows]
            (OUT / f"{path.stem}-reading.txt").write_text("\n".join(rendered) + "\n", encoding="utf-8")

    link_targets = module_paths + ([AFD / "index.html"] if (AFD / "index.html").exists() else [])
    duplicate_ids, broken_links = link_checks(link_targets)
    mechanical = {
        "module_count": len(module_paths),
        "sentence_stats_by_module": stats_by_module,
        "long_sentences_over_35_words": all_long,
        "phrase_occurrences": all_phrases,
        "duplicate_ids": duplicate_ids,
        "broken_local_module_links": broken_links,
    }
    (OUT / "mechanical-rubric-checks.json").write_text(
        json.dumps(mechanical, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Recorded {len(module_paths)} module hashes")
    print(f"Long sentences over 35 words: {len(all_long)}")
    print(f"Rubric phrase occurrences: {len(all_phrases)}")
    print(f"Duplicate ids: {len(duplicate_ids)}")
    print(f"Broken local module links: {len(broken_links)}")


if __name__ == "__main__":
    main()
