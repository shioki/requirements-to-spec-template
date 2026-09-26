#!/usr/bin/env python3
"""skills/ 配下の SKILL.md を Agent Skills 仕様に沿って検査する。

frontmatter は最上位のキーだけを読む。CI に PyYAML が無くても動くよう、
入れ子の値(metadata.tags など)は解釈しない。あわせて
`scripts/sync_skill.py --check` で生成物が正本と一致しているかを確かめる。
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

# Agent Skills 仕様で定義されている最上位キー
KNOWN_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "paths",
    "disable-model-invocation",
    "allowed-tools",
    "model",
    "version",
}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
KEY_RE = re.compile(r"^([A-Za-z][\w-]*):\s*(.*)$")
NAME_MAX = 64
DESCRIPTION_MIN = 20
DESCRIPTION_MAX = 1024


def frontmatter(text: str) -> dict[str, str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    keys: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return keys
        match = KEY_RE.match(line)
        if match:
            keys[match.group(1)] = match.group(2).strip().strip("'\"")
    return None


def check_skill(skill_dir: Path) -> list[str]:
    label = skill_dir.relative_to(REPO_ROOT)
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{label}: SKILL.md がありません"]
    keys = frontmatter(skill_file.read_text(encoding="utf-8"))
    if keys is None:
        return [f"{label}/SKILL.md: YAML frontmatter(--- で囲む)がありません"]

    problems = [f"{label}/SKILL.md: 仕様に無いキー {key}" for key in sorted(keys.keys() - KNOWN_KEYS)]

    name = keys.get("name", "")
    if not name:
        problems.append(f"{label}/SKILL.md: name がありません")
    else:
        if name != skill_dir.name:
            problems.append(f"{label}/SKILL.md: name {name} がフォルダ名 {skill_dir.name} と一致しません")
        if len(name) > NAME_MAX or not NAME_RE.match(name):
            problems.append(f"{label}/SKILL.md: name {name} は {NAME_MAX} 文字以内の kebab-case にしてください")

    description = keys.get("description", "")
    if not DESCRIPTION_MIN <= len(description) <= DESCRIPTION_MAX:
        problems.append(
            f"{label}/SKILL.md: description は {DESCRIPTION_MIN}〜{DESCRIPTION_MAX} 文字にしてください(現在 {len(description)} 文字)"
        )

    explicit_only = keys.get("disable-model-invocation")
    if explicit_only is not None and explicit_only not in ("true", "false"):
        problems.append(f"{label}/SKILL.md: disable-model-invocation は true か false にしてください")
    return problems


def main() -> int:
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
    problems: list[str] = []
    if not skill_dirs:
        problems.append("skills/ にスキルがありません")
    for skill_dir in skill_dirs:
        problems.extend(check_skill(skill_dir))
    for problem in problems:
        print(problem)

    sync = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "sync_skill.py"), "--check"])
    if not problems and sync.returncode == 0:
        print(f"ok: {len(skill_dirs)} スキル")
    return 1 if problems or sync.returncode else 0


if __name__ == "__main__":
    raise SystemExit(main())
