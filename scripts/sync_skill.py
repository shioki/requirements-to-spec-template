#!/usr/bin/env python3
"""ルートの正本から skills/requirements-spec/ の配布用ファイルを生成する。

`gh skill install` はスキルのディレクトリだけを導入するため、テンプレートや
記述ガイドをスキルの中にも置く必要がある。二重管理にならないよう、正本は
ルートのファイルとし、スキル側はこのスクリプトで生成する。

    python3 scripts/sync_skill.py          # 生成する
    python3 scripts/sync_skill.py --check  # 正本と食い違っていれば失敗する
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "requirements-spec"
NOTICE = "生成物: {source} から scripts/sync_skill.py で生成。直接編集しない"

# (正本, 生成先, 本文の置換)
TEXT_FILES: list[tuple[str, str, list[tuple[str, str]]]] = [
    ("template.md", "references/template.md", []),
    ("template-lite.md", "references/template-lite.md", []),
    ("docs/writing-guide.md", "references/writing-guide.md", [("](../template.md)", "](template.md)")]),
    ("scripts/check_ids.py", "scripts/check_ids.py", []),
]
BINARY_DIRS: list[tuple[str, str]] = [
    ("assets/screens/_template", "references/assets/screens/_template"),
]


def render_text(source: str, replacements: list[tuple[str, str]]) -> str:
    text = (REPO_ROOT / source).read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text:
            raise SystemExit(f"{source}: 置換対象が見つかりません: {old}")
        text = text.replace(old, new)
    notice = NOTICE.format(source=source)
    if source.endswith(".py"):
        shebang, _, rest = text.partition("\n")
        return f"{shebang}\n# {notice}\n{rest}"
    return f"<!-- {notice} -->\n\n{text}"


def expected_files() -> dict[Path, bytes]:
    files: dict[Path, bytes] = {}
    for source, target, replacements in TEXT_FILES:
        files[SKILL_DIR / target] = render_text(source, replacements).encode("utf-8")
    for source, target in BINARY_DIRS:
        for path in sorted((REPO_ROOT / source).iterdir()):
            if path.is_file():
                files[SKILL_DIR / target / path.name] = path.read_bytes()
    return files


def generated_roots() -> list[Path]:
    return [SKILL_DIR / "references", SKILL_DIR / "scripts"]


def existing_files() -> set[Path]:
    found: set[Path] = set()
    for root in generated_roots():
        if root.exists():
            found.update(path for path in root.rglob("*") if path.is_file())
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="スキルの配布用ファイルを正本から生成する")
    parser.add_argument("--check", action="store_true", help="生成せず、食い違いがあれば失敗する")
    args = parser.parse_args(argv)

    expected = expected_files()
    stale = sorted(existing_files() - expected.keys())

    if args.check:
        problems = [
            str(path.relative_to(REPO_ROOT))
            for path, content in expected.items()
            if not path.is_file() or path.read_bytes() != content
        ]
        problems += [f"{path.relative_to(REPO_ROOT)}(正本がありません)" for path in stale]
        for problem in problems:
            print(f"未同期: {problem}")
        if problems:
            print("python3 scripts/sync_skill.py を実行してください", file=sys.stderr)
        return 1 if problems else 0

    for path in stale:
        path.unlink()
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.is_file() or path.read_bytes() != content:
            path.write_bytes(content)
    (SKILL_DIR / "scripts" / "check_ids.py").chmod(0o755)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
