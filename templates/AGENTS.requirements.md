<!-- requirements-to-spec-template:begin -->
## 要求仕様

- 要求仕様書は `docs/requirements/` にある。機能を実装・修正する前に、対象の `機能-XX` と受け入れ基準、そこから参照される `権限-XX` / `画面-XX` / `文言-XX` / `非機能-XX` / `データ-XX` を読む
- 仕様書に書かれていない挙動は推測で実装しない。ユーザーに確認し、決まらなければ `未解決-XX` として追加を提案する
- コミットメッセージと Pull Request の説明に、対応する `機能-XX` を書く
- 画面は、画面詳細に書かれた DADS のコンポーネントと、制約条件で固定した DADS の版に従う。表示する文言は `文言-XX` のとおりにする
- 仕様書を変更したら、`requirements-spec` スキルの `scripts/check_ids.py` で整合を検査する
- 要求仕様書の草案は `/draft-spec`、レビューは `/review-spec` で作る
<!-- requirements-to-spec-template:end -->
