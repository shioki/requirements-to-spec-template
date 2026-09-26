# AGENTS.md

Webアプリ開発専用の要求仕様書テンプレート集そのもののリポジトリです。Cursor / Claude Code / Codex など、AGENTS.md を読むエージェント向けの規約をまとめます。`docs/cursor-handoff.md` は v0.2.0 前後の作業指示の記録で、現在のバックログではありません。

## 配布物

`skills/` は、他のプロジェクトへ導入する Agent Skills です(`gh skill install` はリポジトリ直下の `skills/` を探索する)。

- `skills/requirements-spec/references/` と `skills/requirements-spec/scripts/` は生成物。直接編集せず、正本(`template.md`、`template-lite.md`、`docs/writing-guide.md`、`assets/screens/_template/`、`scripts/check_ids.py`)を直してから `python3 scripts/sync_skill.py` を実行する
- `SKILL.md` の frontmatter は Agent Skills 仕様のキーだけを使う。`name` はフォルダ名と同じ kebab-case にする

## ID体系

- プレフィックスは日本語で統一する: `業務-XX` / `利用-XX` / `機能-XX` / `非機能-XX` / `制約-XX` / `連携-XX` / `前提-XX` / `未解決-XX` / `データ-XX` / `画面-XX` / `権限-XX` / `文言-XX` / `運用-XX` / `リスク-XX` / `試験-XX`
- ドキュメントIDは `要件-XXXX`
- 優先度は `必須` / `推奨` / `任意`、スコープは `スコープ内` / `スコープ外`
- 旧英字ID(BR / UC / FR / NFR / TC など)は新規に使わない

## 記述ルール

- 機能要求は「[条件/トリガー] のとき、システムは [動作] する」形式で書く
- 「適切に」「なるべく」「可能な限り」などのあいまい語を使わない
- 未確定事項は本文に書かず `未解決-XX` に切り出し、担当者と期限を付ける
- 括弧は半角 `()` に統一する

## 画面要求の画像

- 格納先: `assets/screens/<プロジェクト識別子>/`(テンプレート用は `_template/`)
- ファイル名: `画面-ID_画面名_状態.<拡張子>`(状態を省略しない)
- 画像には必ず代替テキストを付ける
- プレースホルダーは `scripts/generate_screen_placeholders.py` で生成する(要 `rsvg-convert` と Noto Sans CJK JP)

## Mermaid

- `participant` やノードIDに `Note` / `end` / `loop` / `alt` などの予約語を使わない(詳細は `docs/writing-guide.md` の Mermaid 注意節)

## 変更時の波及チェック

`template.md` の構成・ID・表記を変えたら、次もあわせて更新する。

- `python3 scripts/sync_skill.py` でスキルの生成物を更新する
- `skills/requirements-spec/SKILL.md`(IDの一覧・書くときの規則)
- `README.md`(テンプレート構成・ID対応表)
- `docs/writing-guide.md`(ID凡例・記述ルール)
- `examples/*.md`(記入例)
- `CHANGELOG.md` の `[Unreleased]`

## 品質チェック

- コミット前に `npx markdownlint-cli2 "**/*.md"`、`python3 scripts/check_ids.py examples/*.md`、`python3 scripts/sync_skill.py --check` を実行する(設定は `.markdownlint.jsonc`)
- コミットメッセージは Conventional Commits(`docs:` / `ci:` / `chore:` / `feat:`)、本文は日本語
