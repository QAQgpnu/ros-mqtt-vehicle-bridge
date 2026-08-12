# Maintainer workflow

## Pull requests

1. Keep each PR focused on one behavior or documentation change.
2. Require the quality workflow and a reviewer checklist before merging.
3. Ask for changes when tests, credential hygiene, licensing, or message compatibility are unclear.
4. Squash-merge only after the PR description, tests, and follow-up issues are complete.

## Issues

- Use the bug template for reproducible failures and remove sensitive logs.
- Use the feature template for focused proposals; large changes should start with a roadmap discussion.
- Label issues as `bug`, `enhancement`, `documentation`, or `chore` so release notes stay useful.

## Releases

1. Update `CHANGELOG.md` under `Unreleased`.
2. Merge the release-preparation PR after Actions passes.
3. Create an annotated version tag such as `v0.1.0` and a GitHub Release from that tag.
4. Summarize compatibility, validation, known limitations, and security boundaries.

Do not publish credentials, customer data, proprietary protocol documents, or copied third-party source.

