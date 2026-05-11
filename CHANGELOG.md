# Changelog

All notable changes to this project are documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning.

## Release Update Sequence

```mermaid
sequenceDiagram
  participant Contributor as Contributor
  participant Maintainer as Maintainer
  participant Changelog as CHANGELOG.md
  participant Release as ReleaseTag

  Contributor->>Maintainer: 変更内容をPRで提案
  Maintainer->>Changelog: Added/Changed/Fixedを更新
  Maintainer->>Maintainer: バージョン番号と日付を確定
  Maintainer->>Release: タグ作成と公開
  Release-->>Contributor: リリース内容を共有
```

## [0.1.0] - 2026-05-12

### Added

- Initial public release structure for a MIT-licensed repository
- `template.md` with 11-section requirements-to-spec template
- `examples/order-management-sample.md` as a filled sample
- `docs/writing-guide.md` for writing rules and review checklist
- `LICENSE` (MIT)
- `CONTRIBUTING.md`
- Reworked `README.md` for public GitHub usage
