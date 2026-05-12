#!/usr/bin/env bash
set -euo pipefail

# Claude 작업 지침 설치 스크립트
#
# 사용법 (프로젝트 루트에서):
#   bash <(curl -sSL https://raw.githubusercontent.com/kuks2309/kuks_claude_setup/master/claude_guideline/install.sh)

RAW_URL="https://raw.githubusercontent.com/kuks2309/kuks_claude_setup/master/claude_guideline"
TARGET_DIR="docs/claude_guideline"

if [ ! -d ".git" ]; then
  echo "[!] 현재 디렉토리는 git 저장소가 아닙니다. 프로젝트 루트에서 실행하세요."
  exit 1
fi

if [ -d "$TARGET_DIR" ]; then
  echo "[!] $TARGET_DIR 이미 존재합니다. 업데이트하려면 $TARGET_DIR/update.sh 를 사용하세요."
  exit 1
fi

mkdir -p "$TARGET_DIR/local" "$TARGET_DIR/hooks"

FILES=(
  "README.md"
  "github.md"
  "coding.md"
  "workflow.md"
  "documentation.md"
  "manual.md"
  "ros2.md"
  "tech_debt.md"
  "iteration_anti_pattern.md"
  "skill_update.md"
  "user_instruction_handling_sop.md"
  "claude_md.md"
  "VERSION"
  "CHANGELOG.md"
  "update.sh"
  "audit.sh"
)
for f in "${FILES[@]}"; do
  echo "[+] Downloading $f"
  curl -fsSL "$RAW_URL/$f" -o "$TARGET_DIR/$f"
done

HOOK_FILES=(
  "README.md"
  "session_start_claude_mistake.sh"
)
for f in "${HOOK_FILES[@]}"; do
  echo "[+] Downloading hooks/$f"
  curl -fsSL "$RAW_URL/hooks/$f" -o "$TARGET_DIR/hooks/$f"
done

chmod +x "$TARGET_DIR/update.sh" "$TARGET_DIR/audit.sh" "$TARGET_DIR/hooks/session_start_claude_mistake.sh"

# SOP 가 의존하는 표준 폴더 자동 생성 (documentation.md §docs/ 표준 폴더)
# - claude-mistake/: SSOT 의 README 다운로드 (사건 entry 는 사용자가 작성)
# - user_instructions/: 사용자 지시 누적 기록 (user_instruction_handling_sop.md §3)
# - worklog/: 작업 결과·산출물 기록 (user_instruction_handling_sop.md §9)
mkdir -p docs/claude-mistake docs/user_instructions docs/worklog

if [ ! -f "docs/claude-mistake/README.md" ]; then
  echo "[+] Downloading claude-mistake/README.md"
  curl -fsSL "https://raw.githubusercontent.com/kuks2309/kuks_claude_setup/master/claude-mistake/README.md" \
    -o "docs/claude-mistake/README.md"
fi

if [ ! -f "docs/user_instructions/README.md" ]; then
  cat > "docs/user_instructions/README.md" <<'EOF'
# 사용자 지시 기록 (user_instructions)

사용자가 터미널에 입력한 지시사항의 시간 누적 기록 전용. 형식 SSOT: [user_instruction_handling_sop.md](../claude_guideline/user_instruction_handling_sop.md) §3.

- 사용자 원문 인용만 (요약·해석 금지)
- 시간 역순 (최신 위), KST 시각
- 처리 결과·산출물은 본 폴더 금지 → [worklog/](../worklog/) 또는 `code_review/` / `analysis/` 책임

실제 사용자 지시는 `user_instructions.md` 에 누적.
EOF
fi

if [ ! -f "docs/worklog/README.md" ]; then
  cat > "docs/worklog/README.md" <<'EOF'
# 작업 기록 (worklog)

사용자 지시에 대한 처리 결과·결론·산출물의 시간 누적 기록. 형식 SSOT: [user_instruction_handling_sop.md](../claude_guideline/user_instruction_handling_sop.md) §9 (Step 8).

- 파일 단위: `YYYY-MM-DD.md` (시간 역순)
- 매 entry: `### 트리거 요청` ([user_instructions.md](../user_instructions/user_instructions.md) 참조) + `### 처리` + `### 결론 / 산출물`
- 코드 리뷰 / 분석 / 리팩토링은 본 폴더가 아닌 `code_review/` / `analysis/` / `refactoring/` 책임
EOF
fi

cat > "$TARGET_DIR/local/README.md" <<'EOF'
# 프로젝트별 Override

이 폴더의 파일은 `update.sh` 실행 시 덮어쓰지 않습니다.
프로젝트 고유의 지침은 여기에 별도 파일로 작성하세요.

CLAUDE.md 의 "문서 작업 규칙" 섹션에서 진입 링크를 추가합니다.
EOF

echo ""
echo "[OK] 설치 완료: $TARGET_DIR/"
echo ""
echo "다음 단계:"
echo "  1. CLAUDE.md 의 '문서 작업 규칙' 섹션에 다음 링크를 추가하세요:"
echo "       - 진입점 → docs/claude_guideline/README.md"
echo "  2. 또는 templates/CLAUDE.md.template 을 참고해 새 CLAUDE.md 작성"
echo "  3. 업데이트: bash $TARGET_DIR/update.sh"
echo "  4. docs/ 구조 점검(dry-run): bash $TARGET_DIR/audit.sh"
