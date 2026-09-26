---
name: draft-spec
description: 会議メモやチャットの断片から、Webアプリの要求仕様書の草案を docs/requirements/ に作る。ユーザーが /draft-spec と明示的に入力したときだけ起動する。
disable-model-invocation: true
license: MIT
compatibility: Cursor 3.x, Claude Code, Codex
metadata:
  tags: [requirements, specification, web-app, action]
---

# 要求仕様書の草案を作る

会議メモやチャットの断片を、`requirements-spec` スキルのテンプレートに沿った要求仕様書の草案にします。

## Instructions

### 1. ヒアリング

次を確認してください。会話の中で分かっている項目は聞き直さず、確認だけにします。

- **入力**: 会議メモ、チャット、議事録など(貼り付けまたはファイル)
- **仕様名**: 保存先 `docs/requirements/<仕様名>.md` のファイル名(英小文字とハイフン)
- **テンプレート**: 通常は `template.md`。小規模なら `template-lite.md`

### 2. テンプレートを読む

`requirements-spec` スキルの `references/template.md`(または `references/template-lite.md`)と `references/writing-guide.md` を読みます。スキルは `.agents/skills/`、`.claude/skills/`、`.cursor/skills/` のいずれかにあります。

### 3. 草案を書く

テンプレートの見出し順で書きます。次を守ってください。

- 入力に無い機能や数値を補わない。足りない情報は `未解決-XX` にし、担当者と期限の欄は空欄のまま残す
- 入力の発言を「問題提起」「決定事項」「未解決事項」に分け、本文に書くのは決定事項だけにする
- 機能要求は「[条件/トリガー] のとき、システムは [動作] する」と書き、機能ごとに受け入れ基準(条件、入力、期待結果、異常系、境界値)を書く。合意前なので `[ ]` にする
- 「適切に」「なるべく」「可能な限り」は使わない
- 画面の主要要素は DADS のコンポーネント名で書く。入力から判断できなければ `未解決-XX` にする
- アクセシビリティと対応環境が入力に無い場合も、非機能要求の行は残し、目標値を `未解決-XX` にする
- 括弧は半角 `()` を使う

### 4. 保存と検査

1. `docs/requirements/<仕様名>.md` に保存する。同名のファイルがあれば上書きせず、ユーザーに確認する
2. `docs/requirements/README.md` の一覧に1行追加する
3. `requirements-spec` スキルの `scripts/check_ids.py` で検査し、指摘があれば直す

### 5. 報告

作成したファイル、登録した `未解決-XX` の一覧、検査の結果を報告します。未解決事項は、誰に何を確認すればよいかが分かる形で示してください。
