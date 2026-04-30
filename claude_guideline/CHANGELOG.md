# Changelog

## 1.1.0 — 2026-04-30

- `github.md`: "커밋·푸쉬는 작업 단위로 분리" 섹션 추가
  - 작업 단위 = 커밋 단위 = push 단위 원칙
  - staged 범위 검증 절차 (`git status --short`, `git diff --cached --name-only`)

## 1.0.0 — 2026-04-30

- 초기 릴리스
- `claude_guideline/` 5 개 파일 추가: `README`, `github`, `coding`, `workflow`, `documentation`
- `install.sh`, `update.sh`, `VERSION`, `CHANGELOG.md` 추가
- `templates/CLAUDE.md.template` 추가 (프로젝트별 CLAUDE.md 골격)

## 정책

- **major** (X.0.0): 기존 규칙과 호환 안 됨, 수동 마이그레이션 필요
- **minor** (X.Y.0): 규칙 추가, 호환됨
- **patch** (X.Y.Z): 오탈자, 표현 수정
