#!/usr/bin/env python3
"""要求IDの定義と参照、トレーサビリティの紐付けを検査する。

定義は各表の ID 列。参照は本文中の `業務-01` 形式。
`機能-01〜03` は 機能-01、機能-02、機能-03 に展開する。
`試験-XX` も他のIDと同じく、試験の表の ID 列で定義する。
トレーサビリティ表の試験列は参照として扱う。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PREFIXES = (
    "業務|利用|機能|非機能|制約|連携|前提|未解決|データ|画面|権限|文言|運用|リスク|試験"
)
ID_RE = re.compile(rf"(?:{PREFIXES})-\d{{2}}")
RANGE_RE = re.compile(
    rf"(?P<prefix>{PREFIXES})-(?P<start>\d{{2}})[〜～](?:(?P=prefix)-)?(?P<end>\d{{2}})"
)
SEPARATOR_RE = re.compile(r":?-{3,}:?")


def expand_ids(text: str) -> set[str]:
    found: set[str] = set()
    covered: list[tuple[int, int]] = []
    for match in RANGE_RE.finditer(text):
        start = int(match.group("start"))
        end = int(match.group("end"))
        if start > end:
            continue
        prefix = match.group("prefix")
        for number in range(start, end + 1):
            found.add(f"{prefix}-{number:02d}")
        covered.append(match.span())
    for match in ID_RE.finditer(text):
        if any(span_start <= match.start() < span_end for span_start, span_end in covered):
            continue
        found.add(match.group(0))
    return found


def split_cells(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def is_separator(line: str) -> bool:
    cells = split_cells(line)
    return bool(cells) and all(SEPARATOR_RE.fullmatch(cell) for cell in cells)


def defined_ids(text: str) -> set[str]:
    defined: set[str] = set()
    lines = text.splitlines()
    index = 0
    while index < len(lines) - 1:
        if lines[index].lstrip().startswith("|") and is_separator(lines[index + 1]):
            headers = split_cells(lines[index])
            id_columns = [pos for pos, header in enumerate(headers) if header == "ID"]
            index += 2
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                cells = split_cells(lines[index])
                for column in id_columns:
                    if column < len(cells):
                        defined.update(expand_ids(cells[column]))
                index += 1
            continue
        index += 1
    return defined


def traceability_section(text: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if re.match(r"^##\s+.*トレーサビリティ\s*$", line):
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end])


def traceability_rows(section: str) -> list[str]:
    lines = section.splitlines()
    rows: list[str] = []
    index = 0
    while index < len(lines) - 1:
        if lines[index].lstrip().startswith("|") and is_separator(lines[index + 1]):
            index += 2
            while index < len(lines) and lines[index].lstrip().startswith("|"):
                rows.append(lines[index])
                index += 1
            continue
        index += 1
    return rows


def check_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    defined = defined_ids(text)
    section = traceability_section(text)
    rows = traceability_rows(section)
    traced: set[str] = set()
    linked: set[str] = set()
    for row in rows:
        ids = expand_ids(row)
        row_functions = {item for item in ids if item.startswith("機能-")}
        traced.update(row_functions)
        if any(item.startswith("試験-") for item in ids):
            linked.update(row_functions)

    errors: list[str] = []
    reported: set[tuple[int, str, str]] = set()
    for line_no, line in enumerate(text.splitlines(), start=1):
        for item in sorted(expand_ids(line)):
            if item in defined:
                continue
            key = (line_no, "未定義参照", item)
            if key not in reported:
                reported.add(key)
                errors.append(f"{path}:{line_no}: 未定義参照 {item}")

    for item in sorted(defined):
        if not item.startswith("機能-"):
            continue
        if item not in traced:
            errors.append(f"{path}: 未トレース {item}")
        elif item not in linked:
            errors.append(f"{path}: 試験未紐付け {item}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="要求IDとトレーサビリティの整合を検査する")
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args(argv)

    errors: list[str] = []
    for path in args.files:
        if not path.is_file():
            print(f"{path}: ファイルがありません", file=sys.stderr)
            return 1
        errors.extend(check_file(path))

    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
