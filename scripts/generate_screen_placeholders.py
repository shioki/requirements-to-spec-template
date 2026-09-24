#!/usr/bin/env python3
"""画面要求のプレースホルダー(PNG)を生成するスクリプト。

`assets/screens/` 配下に、文書ごとのサブディレクトリを作成して
プレースホルダー画像(PNG)を生成します。SVGを一時生成して
`rsvg-convert` でPNG化し、SVGは削除します。

サブディレクトリ構成:
  assets/screens/
  ├── _template/         template.md 用の汎用プレースホルダー
  ├── saas-feature/      examples/saas-feature-sample.md 用
  └── order-management/  examples/order-management-sample.md 用
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_ROOT = REPO_ROOT / "assets" / "screens"
FONT_FAMILY = "Noto Sans CJK JP, sans-serif"


def esc(text: str) -> str:
    return escape(text, {'"': "&quot;"})


def svg_document(width: int, height: int, body: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
{body}
</svg>
"""


def background(width: int, height: int) -> str:
    return f'  <rect width="{width}" height="{height}" fill="#f6f7fb"/>'


def header_bar(title: str, *, right: str | None = None, right_size: int = 13, width: int = 800) -> str:
    lines = [
        f'  <rect x="0" y="0" width="{width}" height="56" fill="#1f2a44"/>',
        f'  <text x="24" y="36" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="18" font-weight="bold">{esc(title)}</text>',
    ]
    if right is not None:
        lines.append(
            f'  <text x="{width - 24}" y="36" text-anchor="end" fill="#cdd5e0" font-family="{FONT_FAMILY}" font-size="{right_size}">{esc(right)}</text>'
        )
    return "\n".join(lines)


def footer_label(text: str, *, y: int, x: int = 760) -> str:
    return f'  <text x="{x}" y="{y}" text-anchor="end" fill="#9aa3b5" font-family="{FONT_FAMILY}" font-size="11">{esc(text)}</text>'


def panel(x: int, y: int, width: int, height: int, *, stroke: str = "#d8deea", dashed: bool = False, fill: str = "#ffffff", stroke_width: int | None = None) -> str:
    extra = ""
    if dashed:
        extra += ' stroke-dasharray="6 4"'
    if stroke_width is not None:
        extra += f' stroke-width="{stroke_width}"'
    return f'  <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="12" fill="{fill}" stroke="{stroke}"{extra}/>'


def label(x: int, y: int, text: str, *, size: int = 13, fill: str = "#5a6478", weight: str | None = None, anchor: str | None = None) -> str:
    weight_attr = f' font-weight="{weight}"' if weight else ""
    anchor_attr = f' text-anchor="{anchor}"' if anchor else ""
    return (
        f'  <text x="{x}" y="{y}"{anchor_attr} fill="{fill}" font-family="{FONT_FAMILY}" font-size="{size}"{weight_attr}>{esc(text)}</text>'
    )


def svg_template_screen_01() -> str:
    body = "\n".join([
        background(800, 480),
        header_bar("(アプリ名)", right="プレースホルダー"),
        panel(40, 88, 720, 352, dashed=True),
        label(64, 124, "画面-01 (画面名)", size=20, fill="#1f2a44", weight="bold"),
        label(64, 150, "状態: 初期表示 — 主要要素のワイヤーフレーム"),
        '  <rect x="64" y="184" width="240" height="20" rx="4" fill="#e6e9f1"/>',
        '  <rect x="64" y="216" width="640" height="40" rx="6" fill="#ffffff" stroke="#b9c2d4"/>',
        label(80, 242, "(入力欄1)", fill="#9aa3b5"),
        '  <rect x="64" y="276" width="240" height="20" rx="4" fill="#e6e9f1"/>',
        '  <rect x="64" y="308" width="640" height="40" rx="6" fill="#ffffff" stroke="#b9c2d4"/>',
        label(80, 334, "(入力欄2)", fill="#9aa3b5"),
        '  <rect x="64" y="376" width="160" height="44" rx="6" fill="#2d6cdf"/>',
        label(144, 403, "(主アクション)", size=14, fill="#ffffff", weight="bold", anchor="middle"),
        '  <rect x="240" y="376" width="120" height="44" rx="6" fill="#ffffff" stroke="#b9c2d4"/>',
        label(300, 403, "(キャンセル)", size=14, fill="#5a6478", anchor="middle"),
        footer_label("_template / 画面-01_汎用_初期", y=464),
    ])
    return svg_document(800, 480, body)


def svg_template_screen_02() -> str:
    body = "\n".join([
        background(800, 480),
        header_bar("(アプリ名)", right="プレースホルダー"),
        panel(40, 88, 720, 352, dashed=True),
        label(64, 124, "画面-02 (画面名)", size=20, fill="#1f2a44", weight="bold"),
        label(64, 150, "状態: 確認/結果表示 — 一覧表示のワイヤーフレーム"),
        '  <line x1="64" y1="188" x2="736" y2="188" stroke="#e1e5ee"/>',
        label(64, 212, "(列1)", size=12, weight="bold"),
        label(240, 212, "(列2)", size=12, weight="bold"),
        label(480, 212, "(列3)", size=12, weight="bold"),
        '  <line x1="64" y1="220" x2="736" y2="220" stroke="#eef0f6"/>',
        label(64, 246, "(行1の値)", size=12, fill="#1f2a44"),
        label(240, 246, "(行1の値)", size=12, fill="#1f2a44"),
        label(480, 246, "(行1の値)", size=12, fill="#1f2a44"),
        '  <line x1="64" y1="256" x2="736" y2="256" stroke="#eef0f6"/>',
        label(64, 282, "(行2の値)", size=12, fill="#1f2a44"),
        label(240, 282, "(行2の値)", size=12, fill="#1f2a44"),
        label(480, 282, "(行2の値)", size=12, fill="#1f2a44"),
        '  <line x1="64" y1="292" x2="736" y2="292" stroke="#eef0f6"/>',
        label(64, 318, "(行3の値)", size=12, fill="#1f2a44"),
        label(240, 318, "(行3の値)", size=12, fill="#1f2a44"),
        label(480, 318, "(行3の値)", size=12, fill="#1f2a44"),
        '  <rect x="64" y="376" width="160" height="44" rx="6" fill="#ffffff" stroke="#2d6cdf"/>',
        label(144, 403, "(エクスポート)", size=14, fill="#2d6cdf", weight="bold", anchor="middle"),
        '  <rect x="240" y="376" width="160" height="44" rx="6" fill="#2d6cdf"/>',
        label(320, 403, "(次へ)", size=14, fill="#ffffff", weight="bold", anchor="middle"),
        footer_label("_template / 画面-02_汎用_確認", y=464),
    ])
    return svg_document(800, 480, body)


def svg_saas_share_link_initial() -> str:
    body = "\n".join([
        background(800, 480),
        header_bar("SaaS 管理コンソール", right="admin@example.com", right_size=14),
        panel(40, 88, 720, 352, stroke_width=1),
        label(64, 124, "共有リンクの発行", size=20, fill="#1f2a44", weight="bold"),
        label(64, 150, "期限付きの閲覧専用リンクを発行します(画面-01 / 初期表示)"),
        label(64, 196, "有効期限(最大30日)", size=14, fill="#1f2a44", weight="bold"),
        '  <rect x="64" y="208" width="320" height="40" rx="6" fill="#ffffff" stroke="#b9c2d4"/>',
        label(80, 234, "例: 7日", size=14, fill="#9aa3b5"),
        label(64, 280, "閲覧回数上限(1〜100)", size=14, fill="#1f2a44", weight="bold"),
        '  <rect x="64" y="292" width="320" height="40" rx="6" fill="#ffffff" stroke="#b9c2d4"/>',
        label(80, 318, "例: 10回", size=14, fill="#9aa3b5"),
        '  <rect x="64" y="368" width="140" height="44" rx="6" fill="#c7cde0"/>',
        label(134, 395, "発行(非活性)", size=14, fill="#ffffff", weight="bold", anchor="middle"),
        label(220, 395, "※ 必須項目を入力すると活性化します", size=12),
        footer_label("saas-feature / 画面-01_共有リンク発行_初期", y=464),
    ])
    return svg_document(800, 480, body)


def svg_saas_share_link_denied() -> str:
    body = "\n".join([
        background(800, 480),
        header_bar("ドキュメント共有"),
        panel(120, 120, 560, 280, stroke="#e6c1c1", stroke_width=1),
        '  <circle cx="400" cy="186" r="32" fill="#fbe9e9" stroke="#d24c4c" stroke-width="2"/>',
        label(400, 198, "!", size=32, fill="#d24c4c", weight="bold", anchor="middle"),
        label(400, 256, "このリンクは利用できません", size=20, fill="#1f2a44", weight="bold", anchor="middle"),
        label(400, 286, "リンクの有効期限が切れているか、無効化されています。", size=14, anchor="middle"),
        label(400, 320, "再度共有が必要な場合は、共有元の管理者へお問い合わせください。", anchor="middle"),
        '  <rect x="320" y="346" width="160" height="40" rx="6" fill="#1f2a44"/>',
        label(400, 372, "管理者へ連絡", size=14, fill="#ffffff", weight="bold", anchor="middle"),
        footer_label("saas-feature / 画面-02_閲覧拒否_期限切れ", y=464),
    ])
    return svg_document(800, 480, body)


def svg_order_import_initial() -> str:
    body = "\n".join([
        background(800, 520),
        header_bar("受注管理"),
        panel(40, 88, 720, 160),
        label(64, 124, "受注CSV取り込み", size=20, fill="#1f2a44", weight="bold"),
        label(64, 150, "A社/B社フォーマットの受注CSVを取り込みます(画面-01 / 初期表示)"),
        '  <rect x="64" y="176" width="280" height="44" rx="6" fill="#ffffff" stroke="#b9c2d4" stroke-dasharray="4 4"/>',
        label(204, 203, "ファイルを選択 / ドラッグして配置", anchor="middle"),
        '  <rect x="360" y="176" width="180" height="44" rx="6" fill="#2d6cdf"/>',
        label(450, 203, "取り込み開始", size=14, fill="#ffffff", weight="bold", anchor="middle"),
        panel(40, 272, 720, 216),
        label(64, 304, "過去の取り込み履歴(最新5件)", size=16, fill="#1f2a44", weight="bold"),
        '  <line x1="64" y1="324" x2="736" y2="324" stroke="#e1e5ee"/>',
        label(64, 346, "日時", size=12, weight="bold"),
        label(220, 346, "ファイル名", size=12, weight="bold"),
        label(500, 346, "結果", size=12, weight="bold"),
        label(650, 346, "件数", size=12, weight="bold"),
        '  <line x1="64" y1="356" x2="736" y2="356" stroke="#eef0f6"/>',
        label(64, 380, "2026-05-13 09:12", size=12, fill="#1f2a44"),
        label(220, 380, "A社_受注_20260513.csv", size=12, fill="#1f2a44"),
        label(500, 380, "成功", size=12, fill="#1f8a4b"),
        label(650, 380, "1,024", size=12, fill="#1f2a44"),
        '  <line x1="64" y1="392" x2="736" y2="392" stroke="#eef0f6"/>',
        label(64, 416, "2026-05-12 18:30", size=12, fill="#1f2a44"),
        label(220, 416, "B社_受注_20260512.csv", size=12, fill="#1f2a44"),
        label(500, 416, "エラー(12件)", size=12, fill="#d24c4c"),
        label(650, 416, "498", size=12, fill="#1f2a44"),
        footer_label("order-management / 画面-01_受注取込_初期", y=504),
    ])
    return svg_document(800, 520, body)


def svg_order_error_list() -> str:
    rows = [
        ("12", "受注番号", "必須項目が空欄"),
        ("47", "受注日", "日付フォーマット不正(YYYY/MM/DD想定)"),
        ("88", "受注番号", "既存データと重複"),
        ("103", "金額", "数値以外の文字が含まれる"),
    ]
    row_lines: list[str] = []
    y = 376
    for line_no, col, reason in rows:
        row_lines.append(label(64, y, line_no, size=12, fill="#1f2a44").lstrip())
        row_lines.append(label(160, y, col, size=12, fill="#1f2a44").lstrip())
        row_lines.append(label(320, y, reason, size=12, fill="#d24c4c").lstrip())
        row_lines.append(f'<line x1="64" y1="{y + 8}" x2="736" y2="{y + 8}" stroke="#eef0f6"/>')
        y += 28
    rows_block = "\n  ".join(row_lines)

    body = "\n".join([
        background(800, 560),
        header_bar("受注管理"),
        panel(40, 88, 720, 80, stroke="#e6c1c1", fill="#fff5f5"),
        label(64, 120, "取り込みに失敗しました", size=18, fill="#d24c4c", weight="bold"),
        label(64, 146, "エラー行が 12 件検出されました(画面-02 / エラー一覧)。修正後に再アップロードしてください。"),
        panel(40, 192, 720, 280),
        label(64, 224, "エラー明細(先頭100件まで表示)", size=16, fill="#1f2a44", weight="bold"),
        '  <line x1="64" y1="244" x2="736" y2="244" stroke="#e1e5ee"/>',
        label(64, 266, "行番号", size=12, weight="bold"),
        label(160, 266, "項目名", size=12, weight="bold"),
        label(320, 266, "エラー理由", size=12, weight="bold"),
        '  <line x1="64" y1="276" x2="736" y2="276" stroke="#eef0f6"/>',
        f"  {rows_block}",
        '  <rect x="64" y="496" width="200" height="40" rx="6" fill="#ffffff" stroke="#2d6cdf"/>',
        label(164, 521, "全件CSVダウンロード", size=13, fill="#2d6cdf", weight="bold", anchor="middle"),
        '  <rect x="284" y="496" width="220" height="40" rx="6" fill="#2d6cdf"/>',
        label(394, 521, "修正済CSV再アップロード", size=13, fill="#ffffff", weight="bold", anchor="middle"),
        footer_label("order-management / 画面-02_エラー一覧_エラー", y=544),
    ])
    return svg_document(800, 560, body)


SCREENS: dict[str, list[tuple[str, object]]] = {
    "_template": [
        ("画面-01_汎用_初期", svg_template_screen_01),
        ("画面-02_汎用_確認", svg_template_screen_02),
    ],
    "saas-feature": [
        ("画面-01_共有リンク発行_初期", svg_saas_share_link_initial),
        ("画面-02_閲覧拒否_期限切れ", svg_saas_share_link_denied),
    ],
    "order-management": [
        ("画面-01_受注取込_初期", svg_order_import_initial),
        ("画面-02_エラー一覧_エラー", svg_order_error_list),
    ],
}


def warn_if_font_missing() -> None:
    if shutil.which("fc-list") is None:
        print("warning: fc-list が見つからないため、Noto Sans CJK JP の有無を確認できません", file=sys.stderr)
        return
    result = subprocess.run(["fc-list", "Noto Sans CJK JP"], capture_output=True, text=True, check=False)
    if not result.stdout.strip():
        print(
            "warning: Noto Sans CJK JP がインストールされていません。プレースホルダーの日本語が正しく描画されないことがあります",
            file=sys.stderr,
        )


def render(subdir: str, filename_stem: str, svg_text: str) -> None:
    out_dir = OUT_ROOT / subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    png_path = out_dir / f"{filename_stem}.png"
    with tempfile.NamedTemporaryFile("w", suffix=".svg", encoding="utf-8", delete=False) as tmp:
        tmp.write(svg_text)
        tmp_path = Path(tmp.name)
    try:
        subprocess.run(
            ["rsvg-convert", "-o", str(png_path), str(tmp_path)],
            check=True,
        )
        print(f"generated: {png_path.relative_to(REPO_ROOT)}")
    finally:
        tmp_path.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="画面要求のプレースホルダー(PNG)を生成する")
    parser.add_argument(
        "--only",
        choices=sorted(SCREENS),
        help="生成するサブディレクトリ(_template / saas-feature / order-management)",
    )
    args = parser.parse_args(argv)

    if not shutil.which("rsvg-convert"):
        print("rsvg-convert is required", file=sys.stderr)
        return 1

    warn_if_font_missing()
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    targets = [args.only] if args.only else list(SCREENS)
    for subdir in targets:
        for stem, builder in SCREENS[subdir]:
            render(subdir, stem, builder())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
