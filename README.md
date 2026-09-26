# requirements-to-spec-template

Webアプリ開発の要求を仕様に落とし込むための、GitHub公開向けテンプレート集です。  
会議メモやチャットの断片を、合意可能かつテスト可能な要求仕様書に変換することを目的にしています。

対象は Webアプリ開発に限定しています。新規の Webアプリ開発では、次の3つをそろえて使うことを前提にしています。

- 要求仕様: このリポジトリ
- 知識と判断の記録: [Cursor Knowledge Management System](https://github.com/shioki/Cursor-Knowledge-Management-System)
- 画面設計とアクセシビリティ: [デジタル庁デザインシステム(DADS)](https://design.digital.go.jp/dads/)

Webアプリ以外の要求仕様に使う場合は、汎用テンプレートだった [v0.2.0](https://github.com/shioki/requirements-to-spec-template/releases/tag/v0.2.0) を参照してください。

本リポジトリは、以下の記事の考え方を参考に構成しています。  
[要求を仕様に落とすテンプレートを作ってみた](https://zenn.dev/channnnsm/articles/c3a6de22e71f86)

## Quick Start

1. [`template.md`](template.md) をコピーして、対象プロジェクト名と目的を記入する
2. [`examples/order-management-sample.md`](examples/order-management-sample.md) を参照しながら **業務 → 利用 → 機能** の順で埋める
3. [`docs/writing-guide.md`](docs/writing-guide.md) のチェックリストでレビューし、未確定事項は `未解決-XX` に登録する

### 全体フロー図

```mermaid
flowchart LR
  inputSources["Slack/Notion/会議メモ"] --> defineGoal["目的・スコープを定義"]
  defineGoal --> structureReq["業務→利用→機能を整理"]
  structureReq --> setCriteria["受け入れ基準/非機能を定義"]
  setCriteria --> reviewDoc["チェックリストでレビュー"]
  reviewDoc --> publishSpec["合意済み仕様として運用"]
  reviewDoc --> openIssues["未確定は未解決へ登録"]
  openIssues --> structureReq
```

### 合意形成のシーケンス図

```mermaid
sequenceDiagram
  actor Customer as 顧客
  actor PM as "プロダクトマネージャー(PM)/プロダクトオーナー(PO)"
  actor Team as 開発チーム
  participant Spec as 要求仕様書

  Customer->>PM: 要望と背景を共有
  PM->>Spec: 目的/スコープ/成功指標を記載
  PM->>Team: 業務/利用の確認依頼
  Team->>Spec: 機能/非機能/制約を追記
  Team->>PM: 未確定事項を報告
  PM->>Spec: 未解決として登録(担当/期限)
  PM->>Customer: レビュー依頼
  Customer->>Spec: 承認または差分コメント
```

### 5分で試す最小入力例

```text
業務-01: 受注ミスを月20件以下にする
利用-01: 業務担当者が受注CSVを登録する
機能-01: ユーザーがCSVをアップロードしたとき、システムはフォーマットを検証する
```

### 機能要求の書き方サンプル(悪い例 / 良い例)

```text
悪い例: ユーザーがログインできること
良い例: ユーザーがIDとパスワードを入力して「ログイン」を押下したとき、
    システムは認証を実行し、成功時はダッシュボードに遷移する。
    失敗時は「ログイン情報が正しくありません」と表示する。
```

## このリポジトリでできること

- 要求(Why)と要件/仕様(What)を分離して整理する
- **業務 → 利用 → 機能** の階層で要求を構造化する
- 機能を受け入れ基準付きで定義し、テスト可能にする
- 非機能を数値・条件・測定方法で記述する
- 未確定事項を **未解決事項** として運用管理する
- トレーサビリティ表・データ要求・リスクで抜け漏れを減らす
- Webアプリで漏れやすい役割・権限、画面遷移、画面文言、アクセシビリティ、対応環境、個人情報、運用・移行を要求として書く
- 画面の主要要素を DADS のコンポーネント名で書き、準拠する DADS の版を制約条件で固定する

## 対象読者

- Webアプリの要件定義を標準化したい開発チーム
- 顧客との合意形成に使える仕様書フォーマットが必要なプロダクトマネージャー(PM)/プロダクトオーナー(PO)
- AI実装前に仕様の曖昧さを減らしたいエンジニア

## AI での使い方

- [会議メモから要求仕様書を起こす](docs/prompts/meeting-notes-to-spec.md)
- [仕様書の曖昧語をレビューする](docs/prompts/ambiguity-review.md)

## リポジトリ構成

```text
.
├── README.md
├── template.md
├── template-lite.md
├── assets/
│   └── screens/
│       ├── _template/         # template.md が参照する汎用ワイヤーフレーム
│       ├── saas-feature/      # examples/saas-feature-sample.md 用
│       └── order-management/  # examples/order-management-sample.md 用
├── skills/
│   ├── requirements-spec/     # 要求仕様の Agent Skill(references/ と scripts/ は生成物)
│   ├── draft-spec/            # /draft-spec: 会議メモから草案を作る
│   └── review-spec/           # /review-spec: 曖昧な記述と抜けを指摘する
├── scripts/
│   ├── generate_screen_placeholders.py
│   ├── check_mermaid.py
│   ├── check_ids.py
│   └── sync_skill.py          # 正本から skills/requirements-spec/ の生成物を作る
├── examples/
│   ├── order-management-sample.md
│   └── saas-feature-sample.md
├── docs/
│   ├── writing-guide.md
│   └── prompts/
│       ├── meeting-notes-to-spec.md
│       └── ambiguity-review.md
├── .github/
│   ├── workflows/
│   │   └── lint.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
├── AGENTS.md                  # エージェント向けの規約(Cursor / Claude Code / Codex 共通)
├── CLAUDE.md                  # @AGENTS.md の import のみ
├── .editorconfig
├── .gitignore
├── .lycheeignore
├── .markdownlint.jsonc
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

## サンプル一覧

| ファイル | 内容 |
| --- | --- |
| [`examples/order-management-sample.md`](examples/order-management-sample.md) | 受注CSV取り込みの記入例 |
| [`examples/saas-feature-sample.md`](examples/saas-feature-sample.md) | SaaSの機能追加(共有リンク)の記入例 |
| [`template-lite.md`](template-lite.md) | 小規模案件向けの最小テンプレート(目的・スコープ・業務・利用・機能・未解決) |

## テンプレート構成(`template.md`)

`template.md` の見出しは次のとおりです。

- ID凡例とプレフィックス
- 記入の流れ(参照図)
- レビュー運用シーケンス(参照図)
- ドキュメント管理
- `1. プロジェクト概要`
- `2. ステークホルダー分析`
- `3. 業務要求`
- `4. 利用要求・ユースケース`
- `5. 役割・権限`
- `6. 機能要求`
- `7. 画面要求(UIイメージ)`
- `8. 画面文言`
- `9. 非機能要求`
- `10. 制約条件`
- `11. 外部連携要求`
- `12. 前提条件・依存関係`
- `13. 未解決事項`
- `14. 試験`
- `15. トレーサビリティ`
- `16. データ要求`
- `17. 運用・移行要求`
- `18. リスク`
- `19. 用語定義`
- 変更履歴

## 使い方

1. `template.md` をコピーして新規要求仕様書を作成する。画面画像は `assets/screens/_template/` を参照している。`template.md` だけを別リポジトリへコピーすると画像パスが切れるので、画像ディレクトリも一緒にコピーするか、自プロジェクトの画像に差し替える
2. 「目的」「スコープ内/外」「成功指標」を先に確定する
3. **業務 → 利用 → 機能** の順に詳細化する
4. 機能ごとに受け入れ基準をチェック可能な文で記述する
5. 未確定事項は本文に埋めず `未解決-XX` に移し、担当者と期限を設定する
6. トレーサビリティ表・データ要求・リスクを随時更新する

## 運用ガイド

- 記述ルールとレビュー観点: [`docs/writing-guide.md`](docs/writing-guide.md)
- 記入済みサンプル: [`examples/`](examples/)

## 画面プレースホルダーの再生成(任意)

`examples/` に含まれる画面要求のプレースホルダー画像は、`scripts/generate_screen_placeholders.py` で再生成できます。`rsvg-convert`(librsvg)と Noto Sans CJK JP フォントがインストールされている環境で次を実行してください。

```bash
python3 scripts/generate_screen_placeholders.py
python3 scripts/generate_screen_placeholders.py --only order-management
```

新規プロジェクトでは、本物のキャプチャ/モックアップ画像を `assets/screens/` に直接配置してください(スクリプトの利用は任意です)。

## 品質チェック(Markdown)

Pull Request と `main` への push で、[`.github/workflows/lint.yml`](.github/workflows/lint.yml) が次を実行します。

- `markdownlint-cli2` による Markdown 検査。設定は [`.markdownlint.jsonc`](.markdownlint.jsonc)
- `lychee` によるリンク切れ検査
- `@mermaid-js/mermaid-cli` による Mermaid 構文検査(`scripts/check_mermaid.py`)
- `scripts/check_ids.py` による要求IDとトレーサビリティの整合検査

ローカルではリポジトリルートで次を実行します。

```bash
npx markdownlint-cli2 "**/*.md"
python3 scripts/check_ids.py examples/*.md
```

**任意:** [textlint](https://textlint.github.io/) で技術文書ルールや表記揺れチェックを追加する場合は、チーム方針に合わせて `.textlintrc` を導入してください。

## リリース履歴

- 変更履歴: [CHANGELOG.md](./CHANGELOG.md)

## Issue / PR 運用

- バグ報告: `.github/ISSUE_TEMPLATE/bug_report.md`
- 改善提案: `.github/ISSUE_TEMPLATE/feature_request.md`
- Pull Request: `.github/pull_request_template.md`

## ライセンス

このリポジトリは [MIT License](./LICENSE) で公開しています。

## コントリビューション

改善提案・テンプレート拡張・記入例の追加を歓迎します。  
詳細は [CONTRIBUTING.md](./CONTRIBUTING.md) を参照してください。

## 旧IDから新IDへの対応(破壊的変更)

v0.2.0 で、IDプレフィックスを日本語接頭辞に統一しました。詳細は [CHANGELOG.md](./CHANGELOG.md) の `[0.2.0]` を参照してください。

| 旧ID | 新ID |
| --- | --- |
| BR-XX | 業務-XX |
| UC-XX | 利用-XX |
| FR-XX | 機能-XX |
| NFR-XX | 非機能-XX |
| CON-XX | 制約-XX |
| IF-XX | 連携-XX |
| ASM-XX | 前提-XX |
| OI-XX | 未解決-XX |
| UI-XX(新規) | 画面-XX |
| (v0.3.0 で新規) | 権限-XX |
| (v0.3.0 で新規) | 文言-XX |
| (v0.3.0 で新規) | 運用-XX |
| REQ-XXXX | 要件-XXXX |
| TC-XXX | 試験-XX(v0.3.0 から「試験」の表で定義する) |
| Must / Should / Could | 必須 / 推奨 / 任意 |
| Scope IN / Scope OUT | スコープ内 / スコープ外 |
