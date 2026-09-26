# Changelog

このプロジェクトの重要な変更はすべてこのファイルに記載します。

形式は [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/) に基づき、このプロジェクトは [Semantic Versioning](https://semver.org/lang/ja/) に従います。

## [Unreleased]

### Changed

- `docs/cursor-handoff.md` は当時の記録として残し、v0.4.0 で削除した `.cursor/rules/project-conventions.mdc` へのリンクをリンク検査の対象外にした

## [0.4.0] - 2026-09-26

### Added

- 要求仕様の Agent Skill `skills/requirements-spec/` を追加。仕様書の置き場所(`docs/requirements/`)、実装前に読む箇所、書くときの規則、整合の検査を指示する。テンプレート・記述ガイド・画像・`check_ids.py` は `scripts/sync_skill.py` でルートの正本から生成する
- アクションスキル `/draft-spec`(会議メモから要求仕様書の草案を作る)と `/review-spec`(曖昧な記述と抜けを指摘する)を追加
- `scripts/install.sh --with-agents-md` で、導入先の `AGENTS.md` に要求仕様の節(`templates/AGENTS.requirements.md`)を追記する。実装前に `機能-XX` と受け入れ基準を読むこと、仕様に無い挙動を推測で実装しないことなどを指示する。再実行すると同じ節を置き換える
- 導入スクリプト `scripts/install.sh` を追加。3つのスキルを導入先の `.agents/skills/`(`--skills-dir` で変更可)に置き、`docs/requirements/` と一覧の `README.md` を作る。再実行するとスキルだけを置き換える
- CI に `scripts/check_skills.py` を追加。SKILL.md の frontmatter を Agent Skills 仕様に沿って検査し、スキルの生成物が正本と一致しているかを確かめる
- 未解決事項に `判断記録` 列を追加。解決した理由は Cursor Knowledge Management System の判断記録などに残し、その場所を書く

### Changed

- README に、Webアプリのプロジェクトへの導入手順(導入スクリプトと `gh skill`)を記載
- エージェント向けの規約を `.cursor/rules/project-conventions.mdc`(`alwaysApply: true`)から `AGENTS.md` に移した。`CLAUDE.md` は `@AGENTS.md` の import のみ

## [0.3.0] - 2026-09-26

### Added

- 画面要求に画面遷移図(Mermaid)の節を追加
- 画面詳細の主要要素を DADS のコンポーネント名で書く形にした。DADS に無い要素は「独自」と理由を書く
- 曖昧語レビューのプロンプトに、アクセシビリティ・対応環境・画面文言・未ログイン時の権限・DADS コンポーネント名の抜けを指摘対象として追加
- 運用・移行要求の章(`運用-XX`)を追加。監視・バックアップ・リリース・移行・問い合わせの担当と時期を書き、移行しないデータも明記する
- データ要求に `個人情報` 列を追加。個人情報を含むデータは保持期間後の扱いまで書く
- 試験の章を追加。`試験-XX` を対象・観点・手順・期待結果・種別で定義する
- 制約条件に、準拠する DADS の版とデザイントークンの版(Tailwind CSS を使う場合はテーマプラグインの版も)を固定する例を追加
- 非機能要求にアクセシビリティ(JIS X 8341-3:2016 の適合レベルと試験方法)と対応環境(ブラウザ・OS・画面幅)の行を追加
- 画面文言の章(`文言-XX`)を追加。何が起きたかと次に何をすればよいかを書き、受け入れ基準の異常系から参照する
- 役割・権限の章(`権限-XX`)を追加。未ログインの利用者も役割として書き、表に無い組み合わせは拒否とみなす
- リンク切れチェック(lychee)と Mermaid 構文チェック(`scripts/check_mermaid.py`)を CI に追加
- `.gitignore` を追加
- `template.md` を他リポジトリへコピーするとき、画面画像ディレクトリも一緒にコピーするか自プロジェクトの画像へ差し替える注意を README とテンプレートに記載
- 画面プレースホルダー生成スクリプトの共通部品化、テキストの XML エスケープ、`--only`、Noto Sans CJK JP 未インストール時の警告
- 小規模案件向けの最小テンプレート `template-lite.md` を追加
- AI向けプロンプト例(`docs/prompts/`)を追加。会議メモから要求仕様書を起こす手順と、曖昧語のレビュー
- 要求IDとトレーサビリティの整合を検査する `scripts/check_ids.py` を追加し、CI に組み込んだ

### Changed

- **Breaking:** 役割・権限、画面文言、試験、運用・移行要求の章の追加に伴い、`template.md` の章番号を振り直した
- **Breaking:** `scripts/check_ids.py` は、トレーサビリティ表の試験列を `試験-XX` の定義とみなさなくなった。「試験」の表で定義する
- **Breaking:** 対象を Webアプリ開発に限定した。知識管理の Cursor Knowledge Management System、デジタル庁デザインシステム(DADS)と組み合わせて使う前提にする。Webアプリ以外の用途は v0.2.0 を参照する
- Markdown lint の GitHub Actions を有効化(`.github/workflows/lint.yml`)。サンプルだった `docs/samples/github-actions-markdown-lint.yml` は削除
- README にローカルでの `npx markdownlint-cli2 "**/*.md"` 実行手順を記載
- 表組みを compact スタイルに揃え、強調だけの行を見出しまたは本文にして markdownlint を通過できるようにした
- 非機能要求の参照規格を ISO/IEC 25010:2023(JIS X 25010:2025)に更新した
- `CONTRIBUTING.md` から Issue/PR の項目定義を外し、`.github/` のテンプレートへのリンクだけにした
- `v0.1.0` と `v0.2.0` のタグ作成後、CHANGELOG の compare URL をリンク検査の対象に戻した。`www.iso.org` は CI から 403 になることがあるため除外する
- Mermaid 検査はブラウザ起動のタイムアウト時に 1 回再実行する

## [0.2.0] - 2026-09-25

### Added

- **画面要求(UIイメージ)セクション**を新規追加(`画面-XX` プレフィックス、画面一覧・画面詳細・代替テキスト記述ルール)
- `assets/screens/<プロジェクト識別子>/` を画面キャプチャ・モックアップの格納ディレクトリとして規定(`_template/` / `saas-feature/` / `order-management/` のサブディレクトリで名前空間を分離)
- `scripts/generate_screen_placeholders.py` でプレースホルダー画像(PNG)を再生成可能に
- トレーサビリティ表に `画面` 列を追加
- `docs/writing-guide.md` に画面要求の書き方とレビュー観点を追加

### Changed

- **Breaking:** 要求IDプレフィックスを日本語化(BR→業務、UC→利用 等)。詳細は README の対応表を参照
- **Breaking:** テストケースIDを `試験-XX` に統一(旧英字IDは廃止し、他のIDと同じ2桁連番にする。対応は README を参照)
- **Breaking:** 画面要求セクション追加に伴い `template.md` の章番号を再採番(旧6章「非機能要求」以降が +1)
- テンプレートにトレーサビリティ・データ要求・リスク・Given-When-Then を追加
- 非機能分類に ISO/IEC 25010 参照注記を追加
- `examples/saas-feature-sample.md` / `examples/order-management-sample.md` に画面要求セクションの記入例を追加
- `CONTRIBUTING.md` の見出しを日本語化
- Markdown 用の `.editorconfig` / `.markdownlint.jsonc` と、GitHub Actions 用 lint ワークフローのサンプル(`docs/samples/github-actions-markdown-lint.yml`)を追加

### Fixed

- 表記ゆれ(スコープ表記・優先度表記)の整理

## [0.1.0] - 2026-05-12

### Added

- MIT ライセンスの公開リポジトリ構成
- `template.md`(11セクションの要求仕様テンプレート)
- `examples/order-management-sample.md` の記入例
- `docs/writing-guide.md`(記述ルールとレビューチェックリスト)
- `LICENSE` (MIT)
- `CONTRIBUTING.md`
- 公開向けに整理した `README.md`

[Unreleased]: https://github.com/shioki/requirements-to-spec-template/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/shioki/requirements-to-spec-template/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/shioki/requirements-to-spec-template/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/shioki/requirements-to-spec-template/compare/v0.1.0...v0.2.0

---

## リリース更新の流れ(運用メモ)

```mermaid
sequenceDiagram
  actor Contributor as コントリビュータ
  actor Maintainer as メンテナ
  participant Changelog as CHANGELOG.md
  participant Release as リリースタグ

  Contributor->>Maintainer: 変更内容をPRで提案
  Maintainer->>Changelog: Added/Changed/Fixedを更新
  Maintainer->>Maintainer: バージョン番号と日付を確定
  Maintainer->>Release: タグ作成と公開
  Release-->>Contributor: リリース内容を共有
```
