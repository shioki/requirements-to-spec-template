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

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_ROOT = REPO_ROOT / "assets" / "screens"
FONT_FAMILY = "Noto Sans CJK JP, sans-serif"


# ---------------------------------------------------------------------------
# template.md 用(汎用プレースホルダー)
# ---------------------------------------------------------------------------
def svg_template_screen_01() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 480" width="800" height="480">
  <rect width="800" height="480" fill="#f6f7fb"/>
  <rect x="0" y="0" width="800" height="56" fill="#1f2a44"/>
  <text x="24" y="36" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="18" font-weight="bold">(アプリ名)</text>
  <text x="776" y="36" text-anchor="end" fill="#cdd5e0" font-family="{FONT_FAMILY}" font-size="13">プレースホルダー</text>

  <rect x="40" y="88" width="720" height="352" rx="12" fill="#ffffff" stroke="#d8deea" stroke-dasharray="6 4"/>
  <text x="64" y="124" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="20" font-weight="bold">画面-01 (画面名)</text>
  <text x="64" y="150" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="13">状態: 初期表示 — 主要要素のワイヤーフレーム</text>

  <rect x="64" y="184" width="240" height="20" rx="4" fill="#e6e9f1"/>
  <rect x="64" y="216" width="640" height="40" rx="6" fill="#ffffff" stroke="#b9c2d4"/>
  <text x="80" y="242" fill="#9aa3b5" font-family="{FONT_FAMILY}" font-size="13">(入力欄1)</text>

  <rect x="64" y="276" width="240" height="20" rx="4" fill="#e6e9f1"/>
  <rect x="64" y="308" width="640" height="40" rx="6" fill="#ffffff" stroke="#b9c2d4"/>
  <text x="80" y="334" fill="#9aa3b5" font-family="{FONT_FAMILY}" font-size="13">(入力欄2)</text>

  <rect x="64" y="376" width="160" height="44" rx="6" fill="#2d6cdf"/>
  <text x="144" y="403" text-anchor="middle" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="14" font-weight="bold">(主アクション)</text>

  <rect x="240" y="376" width="120" height="44" rx="6" fill="#ffffff" stroke="#b9c2d4"/>
  <text x="300" y="403" text-anchor="middle" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="14">(キャンセル)</text>

  <text x="760" y="464" text-anchor="end" fill="#9aa3b5" font-family="{FONT_FAMILY}" font-size="11">_template / 画面-01_汎用_初期</text>
</svg>
"""


def svg_template_screen_02() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 480" width="800" height="480">
  <rect width="800" height="480" fill="#f6f7fb"/>
  <rect x="0" y="0" width="800" height="56" fill="#1f2a44"/>
  <text x="24" y="36" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="18" font-weight="bold">(アプリ名)</text>
  <text x="776" y="36" text-anchor="end" fill="#cdd5e0" font-family="{FONT_FAMILY}" font-size="13">プレースホルダー</text>

  <rect x="40" y="88" width="720" height="352" rx="12" fill="#ffffff" stroke="#d8deea" stroke-dasharray="6 4"/>
  <text x="64" y="124" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="20" font-weight="bold">画面-02 (画面名)</text>
  <text x="64" y="150" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="13">状態: 確認/結果表示 — 一覧表示のワイヤーフレーム</text>

  <line x1="64" y1="188" x2="736" y2="188" stroke="#e1e5ee"/>
  <text x="64" y="212" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="12" font-weight="bold">(列1)</text>
  <text x="240" y="212" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="12" font-weight="bold">(列2)</text>
  <text x="480" y="212" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="12" font-weight="bold">(列3)</text>
  <line x1="64" y1="220" x2="736" y2="220" stroke="#eef0f6"/>

  <text x="64" y="246" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">(行1の値)</text>
  <text x="240" y="246" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">(行1の値)</text>
  <text x="480" y="246" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">(行1の値)</text>
  <line x1="64" y1="256" x2="736" y2="256" stroke="#eef0f6"/>

  <text x="64" y="282" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">(行2の値)</text>
  <text x="240" y="282" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">(行2の値)</text>
  <text x="480" y="282" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">(行2の値)</text>
  <line x1="64" y1="292" x2="736" y2="292" stroke="#eef0f6"/>

  <text x="64" y="318" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">(行3の値)</text>
  <text x="240" y="318" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">(行3の値)</text>
  <text x="480" y="318" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">(行3の値)</text>

  <rect x="64" y="376" width="160" height="44" rx="6" fill="#ffffff" stroke="#2d6cdf"/>
  <text x="144" y="403" text-anchor="middle" fill="#2d6cdf" font-family="{FONT_FAMILY}" font-size="14" font-weight="bold">(エクスポート)</text>

  <rect x="240" y="376" width="160" height="44" rx="6" fill="#2d6cdf"/>
  <text x="320" y="403" text-anchor="middle" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="14" font-weight="bold">(次へ)</text>

  <text x="760" y="464" text-anchor="end" fill="#9aa3b5" font-family="{FONT_FAMILY}" font-size="11">_template / 画面-02_汎用_確認</text>
</svg>
"""


# ---------------------------------------------------------------------------
# saas-feature サンプル用
# ---------------------------------------------------------------------------
def svg_saas_share_link_initial() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 480" width="800" height="480">
  <rect width="800" height="480" fill="#f6f7fb"/>
  <rect x="0" y="0" width="800" height="56" fill="#1f2a44"/>
  <text x="24" y="36" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="18" font-weight="bold">SaaS 管理コンソール</text>
  <text x="776" y="36" text-anchor="end" fill="#cdd5e0" font-family="{FONT_FAMILY}" font-size="14">admin@example.com</text>

  <rect x="40" y="88" width="720" height="352" rx="12" fill="#ffffff" stroke="#d8deea" stroke-width="1"/>
  <text x="64" y="124" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="20" font-weight="bold">共有リンクの発行</text>
  <text x="64" y="150" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="13">期限付きの閲覧専用リンクを発行します(画面-01 / 初期表示)</text>

  <text x="64" y="196" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="14" font-weight="bold">有効期限(最大30日)</text>
  <rect x="64" y="208" width="320" height="40" rx="6" fill="#ffffff" stroke="#b9c2d4"/>
  <text x="80" y="234" fill="#9aa3b5" font-family="{FONT_FAMILY}" font-size="14">例: 7日</text>

  <text x="64" y="280" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="14" font-weight="bold">閲覧回数上限(1〜100)</text>
  <rect x="64" y="292" width="320" height="40" rx="6" fill="#ffffff" stroke="#b9c2d4"/>
  <text x="80" y="318" fill="#9aa3b5" font-family="{FONT_FAMILY}" font-size="14">例: 10回</text>

  <rect x="64" y="368" width="140" height="44" rx="6" fill="#c7cde0"/>
  <text x="134" y="395" text-anchor="middle" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="14" font-weight="bold">発行(非活性)</text>
  <text x="220" y="395" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="12">※ 必須項目を入力すると活性化します</text>

  <text x="760" y="464" text-anchor="end" fill="#9aa3b5" font-family="{FONT_FAMILY}" font-size="11">saas-feature / 画面-01_共有リンク発行_初期</text>
</svg>
"""


def svg_saas_share_link_denied() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 480" width="800" height="480">
  <rect width="800" height="480" fill="#f6f7fb"/>
  <rect x="0" y="0" width="800" height="56" fill="#1f2a44"/>
  <text x="24" y="36" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="18" font-weight="bold">ドキュメント共有</text>

  <rect x="120" y="120" width="560" height="280" rx="12" fill="#ffffff" stroke="#e6c1c1" stroke-width="1"/>
  <circle cx="400" cy="186" r="32" fill="#fbe9e9" stroke="#d24c4c" stroke-width="2"/>
  <text x="400" y="198" text-anchor="middle" fill="#d24c4c" font-family="{FONT_FAMILY}" font-size="32" font-weight="bold">!</text>

  <text x="400" y="256" text-anchor="middle" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="20" font-weight="bold">このリンクは利用できません</text>
  <text x="400" y="286" text-anchor="middle" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="14">リンクの有効期限が切れているか、無効化されています。</text>
  <text x="400" y="320" text-anchor="middle" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="13">再度共有が必要な場合は、共有元の管理者へお問い合わせください。</text>

  <rect x="320" y="346" width="160" height="40" rx="6" fill="#1f2a44"/>
  <text x="400" y="372" text-anchor="middle" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="14" font-weight="bold">管理者へ連絡</text>

  <text x="760" y="464" text-anchor="end" fill="#9aa3b5" font-family="{FONT_FAMILY}" font-size="11">saas-feature / 画面-02_閲覧拒否_期限切れ</text>
</svg>
"""


# ---------------------------------------------------------------------------
# order-management サンプル用
# ---------------------------------------------------------------------------
def svg_order_import_initial() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520" width="800" height="520">
  <rect width="800" height="520" fill="#f6f7fb"/>
  <rect x="0" y="0" width="800" height="56" fill="#1f2a44"/>
  <text x="24" y="36" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="18" font-weight="bold">受注管理</text>

  <rect x="40" y="88" width="720" height="160" rx="12" fill="#ffffff" stroke="#d8deea"/>
  <text x="64" y="124" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="20" font-weight="bold">受注CSV取り込み</text>
  <text x="64" y="150" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="13">A社/B社フォーマットの受注CSVを取り込みます(画面-01 / 初期表示)</text>

  <rect x="64" y="176" width="280" height="44" rx="6" fill="#ffffff" stroke="#b9c2d4" stroke-dasharray="4 4"/>
  <text x="204" y="203" text-anchor="middle" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="13">ファイルを選択 / ドラッグして配置</text>

  <rect x="360" y="176" width="180" height="44" rx="6" fill="#2d6cdf"/>
  <text x="450" y="203" text-anchor="middle" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="14" font-weight="bold">取り込み開始</text>

  <rect x="40" y="272" width="720" height="216" rx="12" fill="#ffffff" stroke="#d8deea"/>
  <text x="64" y="304" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="16" font-weight="bold">過去の取り込み履歴(最新5件)</text>

  <line x1="64" y1="324" x2="736" y2="324" stroke="#e1e5ee"/>
  <text x="64" y="346" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="12" font-weight="bold">日時</text>
  <text x="220" y="346" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="12" font-weight="bold">ファイル名</text>
  <text x="500" y="346" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="12" font-weight="bold">結果</text>
  <text x="650" y="346" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="12" font-weight="bold">件数</text>

  <line x1="64" y1="356" x2="736" y2="356" stroke="#eef0f6"/>
  <text x="64" y="380" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">2026-05-13 09:12</text>
  <text x="220" y="380" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">A社_受注_20260513.csv</text>
  <text x="500" y="380" fill="#1f8a4b" font-family="{FONT_FAMILY}" font-size="12">成功</text>
  <text x="650" y="380" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">1,024</text>

  <line x1="64" y1="392" x2="736" y2="392" stroke="#eef0f6"/>
  <text x="64" y="416" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">2026-05-12 18:30</text>
  <text x="220" y="416" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">B社_受注_20260512.csv</text>
  <text x="500" y="416" fill="#d24c4c" font-family="{FONT_FAMILY}" font-size="12">エラー(12件)</text>
  <text x="650" y="416" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">498</text>

  <text x="760" y="504" text-anchor="end" fill="#9aa3b5" font-family="{FONT_FAMILY}" font-size="11">order-management / 画面-01_受注取込_初期</text>
</svg>
"""


def svg_order_error_list() -> str:
    rows = [
        ("12", "受注番号", "必須項目が空欄"),
        ("47", "受注日", "日付フォーマット不正(YYYY/MM/DD想定)"),
        ("88", "受注番号", "既存データと重複"),
        ("103", "金額", "数値以外の文字が含まれる"),
    ]
    row_svg = []
    y = 376
    for line_no, col, reason in rows:
        row_svg.append(
            f'<text x="64" y="{y}" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">{line_no}</text>'
            f'<text x="160" y="{y}" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="12">{col}</text>'
            f'<text x="320" y="{y}" fill="#d24c4c" font-family="{FONT_FAMILY}" font-size="12">{reason}</text>'
        )
        row_svg.append(f'<line x1="64" y1="{y + 8}" x2="736" y2="{y + 8}" stroke="#eef0f6"/>')
        y += 28

    rows_block = "\n  ".join(row_svg)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 560" width="800" height="560">
  <rect width="800" height="560" fill="#f6f7fb"/>
  <rect x="0" y="0" width="800" height="56" fill="#1f2a44"/>
  <text x="24" y="36" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="18" font-weight="bold">受注管理</text>

  <rect x="40" y="88" width="720" height="80" rx="12" fill="#fff5f5" stroke="#e6c1c1"/>
  <text x="64" y="120" fill="#d24c4c" font-family="{FONT_FAMILY}" font-size="18" font-weight="bold">取り込みに失敗しました</text>
  <text x="64" y="146" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="13">エラー行が 12 件検出されました(画面-02 / エラー一覧)。修正後に再アップロードしてください。</text>

  <rect x="40" y="192" width="720" height="280" rx="12" fill="#ffffff" stroke="#d8deea"/>
  <text x="64" y="224" fill="#1f2a44" font-family="{FONT_FAMILY}" font-size="16" font-weight="bold">エラー明細(先頭100件まで表示)</text>

  <line x1="64" y1="244" x2="736" y2="244" stroke="#e1e5ee"/>
  <text x="64" y="266" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="12" font-weight="bold">行番号</text>
  <text x="160" y="266" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="12" font-weight="bold">項目名</text>
  <text x="320" y="266" fill="#5a6478" font-family="{FONT_FAMILY}" font-size="12" font-weight="bold">エラー理由</text>
  <line x1="64" y1="276" x2="736" y2="276" stroke="#eef0f6"/>

  {rows_block}

  <rect x="64" y="496" width="200" height="40" rx="6" fill="#ffffff" stroke="#2d6cdf"/>
  <text x="164" y="521" text-anchor="middle" fill="#2d6cdf" font-family="{FONT_FAMILY}" font-size="13" font-weight="bold">全件CSVダウンロード</text>

  <rect x="284" y="496" width="220" height="40" rx="6" fill="#2d6cdf"/>
  <text x="394" y="521" text-anchor="middle" fill="#ffffff" font-family="{FONT_FAMILY}" font-size="13" font-weight="bold">修正済CSV再アップロード</text>

  <text x="760" y="544" text-anchor="end" fill="#9aa3b5" font-family="{FONT_FAMILY}" font-size="11">order-management / 画面-02_エラー一覧</text>
</svg>
"""


# ---------------------------------------------------------------------------
# レンダラ
# ---------------------------------------------------------------------------
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


def main() -> int:
    if not shutil.which("rsvg-convert"):
        print("rsvg-convert is required", file=sys.stderr)
        return 1

    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    render("_template", "画面-01_汎用_初期", svg_template_screen_01())
    render("_template", "画面-02_汎用_確認", svg_template_screen_02())

    render("saas-feature", "画面-01_共有リンク発行_初期", svg_saas_share_link_initial())
    render("saas-feature", "画面-02_閲覧拒否_期限切れ", svg_saas_share_link_denied())

    render("order-management", "画面-01_受注取込_初期", svg_order_import_initial())
    render("order-management", "画面-02_エラー一覧", svg_order_error_list())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
