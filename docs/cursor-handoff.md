# Cursor 引き継ぎ: 改善バックログ

作成日: 2026-09-25  
対象コミット: `f619992`(docs: 画面要求テンプレートとサンプル画像を追加)

このドキュメントは、リポジトリ全体をレビューして見つかった改善点を、Cursor で順に作業できる形でまとめたものです。
プロジェクト規約は [`.cursor/rules/project-conventions.mdc`](../.cursor/rules/project-conventions.mdc) を参照してください。

## 現状サマリ

- 要求仕様書テンプレート集(Markdown 中心 + 画像生成スクリプト 1 本)
- 直近 2 コミットで「IDの日本語化」「画面要求セクション追加」という破壊的変更が入ったが、`CHANGELOG.md` の `[Unreleased]` のまま未リリース
- Markdown lint の CI はサンプル(`docs/samples/`)として置かれているだけで未有効化
- ドキュメント間(README / template / writing-guide / examples)に細かな不整合がある

## 決定事項(2026-09-25 メンテナ確認済み)

- テストケースIDは **`試験-XX`** に統一する(P1-6)
- **v0.2.0** は推奨どおりに進める: P1 をすべて反映してからリリースする(P2-1)
- P2-4 も推奨どおり、リンクチェックと Mermaid 構文チェックの両方を導入する
- **P3 もすべて実施する**。P3 の成果は v0.2.0 には含めず、次の `[Unreleased]` に記録する

## 作業の進め方

- 作業順: **P1 → P2-1(v0.2.0 リリース)→ P2-2(CI)→ P2 の残り → P3**
- 1 項目 = 1 コミット。既存履歴に合わせて Conventional Commits(`docs:` / `ci:` / `chore:` / `feat:`)を使う
- `template.md` を変更したら README・writing-guide・examples・CHANGELOG への波及を必ず確認する
- 各コミット前に `npx markdownlint-cli2 "**/*.md"` を実行する

---

## P1: 整合性の不具合(優先して修正)

### P1-1 README「テンプレート構成」の番号が template.md と不一致

- 対象: `README.md`
- 内容: README は 1〜18 の通し番号で列挙しているが、`template.md` の実見出しは「ID凡例」「ドキュメント管理」が番号なし、本文が 1〜15、末尾に「変更履歴」。読者が章番号で参照すると食い違う
- 完了条件: README の一覧が `template.md` の見出し(番号含む)と 1 対 1 で一致する

### P1-2 画像ファイル名が命名規則に違反

- 対象: `assets/screens/order-management/画面-02_エラー一覧.png`、`scripts/generate_screen_placeholders.py`、`examples/order-management-sample.md`
- 内容: 規則は `画面-ID_画面名_状態.<拡張子>` だが、状態が欠けている
- 対応: `画面-02_エラー一覧_エラー.png` 等にリネームし、スクリプトの `render(...)` 呼び出しとサンプルの画像参照を更新
- 完了条件: `grep -rn "画面-02_エラー一覧.png" .` が 0 件、`python3 scripts/generate_screen_placeholders.py` 再実行後に `git status` で意図しない差分がない

### P1-3 サンプルの受け入れ基準が一部の機能にしかない

- 対象: `examples/order-management-sample.md`(機能-03 / 機能-04 が欠落)、`examples/saas-feature-sample.md`(機能-02 / 機能-03 が欠落)
- 内容: writing-guide の「機能ごとに受け入れ基準を書く」ルールをサンプル自身が満たしていない
- 完了条件: 両サンプルの機能要求一覧にあるすべての `機能-XX` に「受け入れ基準」節がある

### P1-4 受け入れ基準の見出しレベル・チェックボックスの意味が不統一

- 対象: `examples/*.md`、`docs/writing-guide.md`
- 内容:
  - テンプレートは `### 5.x 受け入れ基準` の下に `#### 機能-XX 受け入れ基準`、サンプルは `### 機能-XX 受け入れ基準`
  - order サンプルは `- [x]`、saas サンプルは `- [ ]` で、チェックの意味(レビュー済? 実装済? テスト合格?)が定義されていない
- 対応: 見出し構造をテンプレートに揃える。チェックの意味(例: `[x]` = レビューで合意済み)を writing-guide 2.3 に明記し、サンプルを統一
- 完了条件: サンプルの見出し階層がテンプレートと一致し、チェックの意味が writing-guide に記載されている

### P1-5 サンプルに「変更履歴」節がない

- 対象: `examples/*.md`
- 内容: `template.md` 末尾にある「変更履歴」表が両サンプルに存在しない
- 完了条件: 両サンプル末尾に変更履歴表がある(記入例 1〜2 行)

### P1-6 テストケースIDが日本語ID凡例に含まれていない

- 対象: `template.md`、`docs/writing-guide.md`、`README.md`(旧ID→新ID対応表)
- 内容: トレーサビリティ表で `TC-001` / `TC-CSV-001` / `TC-SHARE-001` を使っているが、ID凡例は日本語プレフィックスのみ
- 対応(**決定: `試験-XX` に統一**):
  - `template.md` と `docs/writing-guide.md` の ID 凡例に `試験-XX` | 試験(テストケース)| 受け入れ基準を検証するテストケース を追加
  - トレーサビリティ表の列名「テスト観点/ケースID」を「試験」に変更し、`TC-001` → `試験-01` に置換
  - サンプルの `TC-CSV-001` / `TC-CSV-002` / `TC-SHARE-001` / `TC-SHARE-002` を `試験-01` / `試験-02` に置換(ID はドキュメント内で一意なら十分なので、他の ID と同じ 2 桁連番にする)
  - README の旧ID→新ID対応表に `TC-XXX` → `試験-XX` を追加
  - CHANGELOG `[Unreleased]` の Changed に Breaking として追記
- 完了条件: `grep -rn "TC-" --include=*.md .` が 0 件(`docs/cursor-handoff.md` を除く)、凡例とトレーサビリティ表の ID 体系が一致している

### P1-7 writing-guide 4 章の構成と括弧表記

- 対象: `docs/writing-guide.md`
- 内容:
  - 「4.3 Mermaid(予約語・識別子の注意)」が 4.2 と「ステップ1〜4」の間に割り込んでいて、手順の流れが分断されている
  - 4.3 のみ全角括弧 `（）` を使っており、他は半角 `()`(全角括弧は 4 箇所)
- 対応: 「ステップ1〜4」を `4.3 手順` 配下にまとめ、Mermaid の注意は `4.4` へ移動。括弧は半角に統一
- 完了条件: 4 章の見出しが 4.1 → 4.2 → 4.3 → 4.4 の順で並び、`grep -c "（" docs/writing-guide.md` が 0

### P1-8 README 末尾の「次リリースで」表記

- 対象: `README.md`(「旧IDから新IDへの対応(破壊的変更)」節)
- 内容: 「次リリースで〜統一します」が未来形のまま
- 対応: P2-1 のリリースと同時に「v0.2.0 で〜統一しました」へ更新
- 完了条件: README と CHANGELOG のバージョン表記が一致している

---

## P2: 運用・品質

### P2-1 v0.2.0 をリリースする

- 対象: `CHANGELOG.md`
- 内容: `[Unreleased]` に破壊的変更が溜まっている。semver 0.x のため minor 上げ(0.2.0)で可
- 対応(**決定: 推奨どおり進める**):
  1. P1 の全項目(特に破壊的変更の P1-6 `試験-XX`)を反映してから着手する
  2. 見出しを `## [0.2.0] - <リリース作業日>` にし、その上に空の `## [Unreleased]` を残す
  3. ファイル末尾に比較リンク(`[Unreleased]: .../compare/v0.2.0...HEAD`、`[0.2.0]: .../compare/v0.1.0...v0.2.0`)を追加。`v0.1.0` タグが無ければメンテナに確認する
  4. P1-8 の README 表記を同じコミットで更新する
  5. `chore: v0.2.0 をリリース` でコミット後、メンテナが `v0.2.0` タグを付けて GitHub Release を作成する(Cursor はタグを push しない)
- 完了条件: CHANGELOG に 0.2.0 の節と比較リンクがあり、README の表記と一致している

### P2-2 markdownlint CI を有効化する

- 対象: `docs/samples/github-actions-markdown-lint.yml` → `.github/workflows/lint.yml`
- 内容: サンプルとして置いてあるだけで CI が動いていない。`DavidAnson/markdownlint-cli2-action@v16` は古い可能性がある
- 対応: `.github/workflows/lint.yml` として配置し、action の最新メジャーバージョンを確認して更新。README の説明を「有効化済み」に変更(サンプルファイルは削除または README から参照を外す)
- 注意: push に `workflow` スコープ付きトークンが必要な場合がある
- 完了条件: PR 作成時に lint ジョブが実行され、現状の Markdown がすべて通過する

### P2-3 ローカルでの lint 実行手順を明記

- 対象: `README.md`、(任意)`.markdownlint-cli2.jsonc`
- 対応: `npx markdownlint-cli2 "**/*.md"` を README に記載。除外対象が必要なら `.markdownlint-cli2.jsonc` で定義
- 完了条件: README の手順をそのまま実行して lint が完走する

### P2-4 リンク切れ・Mermaid 構文チェックの追加

- 対象: `.github/workflows/`
- 内容: README / docs / examples に外部リンクと Mermaid 図が多い
- 対応(**決定: 推奨どおり両方導入する**):
  - リンクチェック: `lycheeverse/lychee-action` を P2-2 の lint ワークフローに別ジョブとして追加。外部サイトの一時的な障害で落ちないよう、リトライ設定と `.lycheeignore`(必要な除外のみ)を用意する
  - Mermaid 構文チェック: `@mermaid-js/mermaid-cli`(`mmdc`)で全 Markdown 内の Mermaid 図をレンダリングし、失敗したら CI を落とす。対象ファイルの抽出は `scripts/` に小さなスクリプトを置くか、`mmdc -i <file>.md` の Markdown 入力を使う
  - action / パッケージのバージョンは導入時点の最新を確認して固定する
- 完了条件: わざとリンクを壊した場合と Mermaid 図を壊した場合に、それぞれ CI が失敗することを確認済み。現状のリポジトリでは CI が通る

### P2-5 `.gitignore` の追加

- 内容: `.gitignore` が存在しない
- 対応: `__pycache__/`、`.DS_Store`、`*.svg.tmp`、エディタ設定などを追加
- 完了条件: `.gitignore` がリポジトリルートにある

### P2-6 ISO/IEC 25010 の参照を 2023 年版へ更新

- 対象: `template.md` 7 章、`docs/writing-guide.md` 2.4
- 内容: リンク先 `https://www.iso.org/standard/35733.html` は 2011 年版。2023 年版(ISO/IEC 25010:2023)が発行済み
- 対応: リンクを 2023 年版に更新し、品質特性の変更点(例: 安全性の追加、使用性の名称変更など)を注記。**正式な日本語名称は JIS / 公式資料で要確認**
- 完了条件: リンクが 2023 年版を指し、分類例が 2023 年版の特性名と矛盾しない

### P2-7 CONTRIBUTING のテンプレート二重管理を解消

- 対象: `CONTRIBUTING.md`
- 内容: 「Issue/PR 作成時の推奨テンプレート」が `.github/ISSUE_TEMPLATE/` と `.github/pull_request_template.md` の内容と重複・乖離している
- 対応: CONTRIBUTING からは実テンプレートへのリンクのみにする
- 完了条件: テンプレートの項目定義が `.github/` 側だけにある

---

## P3: 利便性・拡張(実施決定済み、v0.2.0 リリース後に着手)

各項目の変更は CHANGELOG の `[Unreleased]` に `Added` / `Changed` として記録する。

### P3-1 テンプレートを他リポにコピーした際の画像パス

- 対象: `README.md`(使い方)、`template.md`(6.2 の注記)
- 内容: `template.md` だけをコピーすると `assets/screens/_template/...` の参照が切れる
- 対応: 「画像ディレクトリも一緒にコピーするか、自プロジェクトの画像に差し替える」旨を明記
- 完了条件: README の使い方に注意書きがある

### P3-2 画像生成スクリプトのリファクタリング

- 対象: `scripts/generate_screen_placeholders.py`
- 内容:
  - ヘッダー帯・枠・フッター表記などの SVG 断片が関数ごとに重複している
  - テキストを XML エスケープしていない(`&` や `<` を含む文言で壊れる)
- 対応: 共通部品を関数化、`html.escape` / `xml.sax.saxutils.escape` でエスケープ、`--only <subdir>` 引数の追加、Noto Sans CJK JP 未インストール時の警告(`fc-list` で確認)
- 完了条件: リファクタ前後で生成 PNG に見た目の差がない(目視確認)

### P3-3 最小版テンプレートの追加

- 内容: 小規模案件向けに「目的 / スコープ / 業務 / 利用 / 機能(受け入れ基準) / 未解決」だけの `template-lite.md` を用意
- 完了条件: README のサンプル一覧・構成図に追加されている

### P3-4 AI 向けプロンプト例の追加

- 内容: README の対象読者に「AI実装前に仕様の曖昧さを減らしたいエンジニア」とあるが、AI 活用の具体例がない
- 対応: `docs/prompts/` に「会議メモ → 要求仕様書」「仕様書の曖昧語レビュー」などのプロンプト例を追加
- 完了条件: README からリンクされている

### P3-5 ID・トレーサビリティ整合チェックスクリプト

- 内容: 手作業だと、定義されていない ID の参照や、トレーサビリティ表に現れない `機能-XX` が発生しやすい
- 対応: `scripts/check_ids.py` を追加。定義済み ID(各表の ID 列)と参照 ID を突き合わせ、未定義参照・未トレース機能・`試験-XX` が紐付いていない機能を列挙。P2-2 の CI に組み込む
- 完了条件: `python3 scripts/check_ids.py examples/*.md` がサンプルに対してエラー 0 件で完走する
