---
name: requirements-spec
description: Webアプリの要求仕様書(docs/requirements/)を作成・更新・参照するときに使用。機能を実装・修正する前に対象の機能-XX と受け入れ基準を確認するとき、業務-XX・機能-XX・画面-XX などの要求IDが話題に出たときにも読み込む。
license: MIT
compatibility: Cursor 3.x, Claude Code, Codex
metadata:
  tags: [requirements, specification, web-app, dads, accessibility]
---

# 要求仕様

Webアプリの要求仕様書を、合意可能でテスト可能な形で書き、実装の根拠として参照するためのスキルです。画面はデジタル庁デザインシステム(DADS)を前提にします。

## When to Use

- 要求仕様書を新しく作る、または更新するとき
- 機能を実装・修正する前に、対象の `機能-XX` と受け入れ基準を確認するとき
- `業務-XX` / `機能-XX` / `画面-XX` などの要求IDが会話に出たとき
- 仕様書の整合(未定義のID、試験の紐付け)を検査するとき

## Instructions

### 1. 仕様書の置き場所

- 仕様書は `docs/requirements/<仕様名>.md` に置く。一覧は `docs/requirements/README.md`
- 画面の画像は `docs/requirements/assets/screens/<プロジェクト識別子>/` に置く
- 新しく作るときは、このスキルの `references/template.md` をコピーする。小規模なら `references/template-lite.md` を使う
- `references/template.md` は `assets/screens/_template/` の画像を参照している。コピーしたら自プロジェクトの画像に差し替える

### 2. 実装の前に読む

機能を実装・修正するときは、コードより先に仕様書の次の箇所を読んでください。

1. 対象の `機能-XX` の行と、その受け入れ基準(`#### 機能-XX 受け入れ基準`)
2. 備考や受け入れ基準から参照されている `権限-XX`、`画面-XX`、`文言-XX`、`非機能-XX`、`データ-XX`
3. 対象を検証する `試験-XX`

仕様書に書かれていない挙動は、推測で実装しないでください。ユーザーに確認し、決まらなければ `未解決-XX` として追加を提案します。コミットメッセージと Pull Request の説明には、対応する `機能-XX` を書きます。

画面を作るときは、画面詳細の主要要素に書かれた DADS のコンポーネントを使い、制約条件で固定した DADS の版に従います。表示する文言は `文言-XX` のとおりにします。

### 3. 書くときの規則

詳細は `references/writing-guide.md` にあります。最低限、次を守ってください。

- IDは日本語のプレフィックスを使う: `業務` / `利用` / `機能` / `非機能` / `制約` / `連携` / `前提` / `未解決` / `データ` / `画面` / `権限` / `文言` / `運用` / `リスク` / `試験`(2桁の連番。例: `機能-01`)
- 機能要求は「[条件/トリガー] のとき、システムは [動作] する」と書く
- 機能ごとに受け入れ基準(条件、入力、期待結果、異常系、境界値)を書く。`[x]` はレビューで合意済み、`[ ]` は未合意
- 「適切に」「なるべく」「可能な限り」は使わない。数値・条件・測定方法で書く
- 未確定の事項は本文に書かず、`未解決-XX` に担当者と期限を付けて登録する
- 非機能要求にアクセシビリティ(JIS X 8341-3:2016 の適合レベルと試験方法)と対応環境を必ず書く
- 括弧は半角 `()` を使う

### 4. 整合の検査

仕様書を変更したら、このスキルの `scripts/check_ids.py` で検査します。未定義のIDの参照、トレーサビリティ表に無い機能、試験が紐付いていない機能を報告します。

```bash
python3 .agents/skills/requirements-spec/scripts/check_ids.py docs/requirements/*.md
```

スキルを `.claude/skills/` や `.cursor/skills/` に置いた場合は、パスを読み替えてください。

### 5. 決めた理由を残す

`未解決-XX` を解決したら、`状態` を `解決済` にし、決めた内容を本文に反映します。なぜそう決めたかは判断記録に残し、その場所を `判断記録` 列に書きます。Cursor Knowledge Management System を導入している場合は `/record-decision` で `decisions/YYYY-MM-DD-スラッグ.md` を作ります。

### 6. 関連するアクションスキル

- `/draft-spec`: 会議メモやチャットから要求仕様書の草案を作る
- `/review-spec`: 要求仕様書の曖昧な記述と抜けを指摘する

記入例は [requirements-to-spec-template の examples/](https://github.com/shioki/requirements-to-spec-template/tree/main/examples) にあります。
