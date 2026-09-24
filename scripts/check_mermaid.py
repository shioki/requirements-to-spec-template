#!/usr/bin/env python3
"""Markdown 内の Mermaid 図を mmdc でレンダリングし、構文エラーがあれば失敗する。"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MERMAID_BLOCK = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)
SKIP_DIRS = {".git", "node_modules"}


def mermaid_files() -> list[Path]:
    files: list[Path] = []
    for path in sorted(REPO_ROOT.rglob("*.md")):
        if SKIP_DIRS.intersection(path.relative_to(REPO_ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8")
        if "```mermaid" in text:
            files.append(path)
    return files


def puppeteer_config(directory: Path) -> Path:
    config: dict[str, object] = {
        "args": ["--no-sandbox", "--disable-dev-shm-usage"],
    }
    chrome = os.environ.get("CHROME_PATH") or shutil.which("chromium") or shutil.which("google-chrome")
    if chrome:
        config["executablePath"] = chrome
    path = directory / "puppeteer-config.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    return path


def mmdc_command() -> list[str]:
    override = os.environ.get("MMDC")
    if override:
        return [override]
    found = shutil.which("mmdc")
    if found:
        return [found]
    return ["npx", "--yes", "-p", "@mermaid-js/mermaid-cli@12.0.0", "mmdc"]


def main() -> int:
    files = mermaid_files()
    if not files:
        print("no mermaid diagrams found", file=sys.stderr)
        return 1

    command = mmdc_command()
    failures = 0
    with tempfile.TemporaryDirectory(prefix="mermaid-check-") as tmp:
        tmp_dir = Path(tmp)
        config = puppeteer_config(tmp_dir)
        for path in files:
            output = tmp_dir / f"{path.stem}.md"
            result = subprocess.run(
                [
                    *command,
                    "-i",
                    str(path),
                    "-o",
                    str(output),
                    "-p",
                    str(config),
                    "-e",
                    "svg",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            relative = path.relative_to(REPO_ROOT)
            if result.returncode != 0:
                failures += 1
                print(f"failed: {relative}", file=sys.stderr)
                if result.stderr.strip():
                    print(result.stderr.strip(), file=sys.stderr)
                elif result.stdout.strip():
                    print(result.stdout.strip(), file=sys.stderr)
            else:
                print(f"ok: {relative}")

    if failures:
        print(f"{failures} file(s) failed mermaid check", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
