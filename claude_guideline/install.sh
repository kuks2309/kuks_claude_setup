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

# docs/ 표준 폴더 전체 자동 생성 (documentation.md §docs/ 표준 폴더, v1.8.6)
# 각 폴더에 역할·SSOT 링크를 담은 stub README 자동 배치 (기존 README 는 덮어쓰지 않음)
mkdir -p \
  docs/architecture \
  docs/usage \
  docs/issues_and_fixes \
  docs/assets \
  docs/user_instructions \
  docs/worklog \
  docs/claude-mistake \
  docs/code_review \
  docs/refactoring \
  docs/analysis \
  docs/test \
  docs/troubleshooting \
  docs/api

if [ ! -f "docs/claude-mistake/README.md" ]; then
  echo "[+] Downloading claude-mistake/README.md"
  curl -fsSL "https://raw.githubusercontent.com/kuks2309/kuks_claude_setup/master/claude-mistake/README.md" \
    -o "docs/claude-mistake/README.md"
fi

write_stub() {
  local path="$1"; local title="$2"; local body="$3"
  [ -f "$path" ] && return 0
  printf '# %s\n\n%s\n' "$title" "$body" > "$path"
}

write_stub docs/architecture/README.md "구조 · 설계 (architecture)" \
  "프로젝트 / 워크스페이스의 구조·설계 문서. ROS2 워크스페이스는 [documentation.md](../claude_guideline/documentation.md) §ROS2 특칙 참조 (패키지별 설계는 \`src/<pkg>/docs/architecture/\`)."

write_stub docs/usage/README.md "설치 · 실행 · 튜토리얼 (usage)" \
  "설치 / 실행 / 사용 가이드. 단일 \`.md\` 파일 (\`INSTALLATION.md\`, \`USER_GUIDE.md\` 등) 흡수 대상."

write_stub docs/issues_and_fixes/README.md "이슈 · 수정 기록 (issues_and_fixes)" \
  "이슈 발생 · 분석 · 수정 결과를 시간 누적 (최신 위). 형식: \`YYYY-MM-DD.md\` 또는 \`YYYY-MM-DD_<짧은제목>.md\`."

write_stub docs/assets/README.md "이미지 · 동영상 · 다이어그램 (assets)" \
  "스크린샷, RViz 캡처, 다이어그램 등 바이너리 리소스. 본문 \`.md\` 와 분리하여 보관."

write_stub docs/user_instructions/README.md "사용자 지시 기록 (user_instructions)" \
  "사용자가 터미널에 입력한 지시사항의 시간 누적 기록 전용. 형식 SSOT: [user_instruction_handling_sop.md](../claude_guideline/user_instruction_handling_sop.md) §3. 사용자 원문 인용만 (요약·해석 금지). 처리 결과·산출물은 [worklog/](../worklog/) 또는 \`code_review/\` / \`analysis/\` 책임. 실제 지시는 \`user_instructions.md\` 에 누적."

write_stub docs/worklog/README.md "작업 기록 (worklog)" \
  "사용자 지시에 대한 처리 결과·결론·산출물 시간 누적 기록. 형식 SSOT: [user_instruction_handling_sop.md](../claude_guideline/user_instruction_handling_sop.md) §9. 파일: \`YYYY-MM-DD.md\`. 매 entry 는 \`### 트리거 요청\` ([user_instructions.md](../user_instructions/user_instructions.md) 참조) + \`### 처리\` + \`### 결론 / 산출물\`."

write_stub docs/code_review/README.md "코드 리뷰 결과 (code_review)" \
  "코드 리뷰·외부 advisor (Codex/Gemini ccg) 결과 리포트. \`code-review/\` / \`code_reivew/\` 변종은 본 폴더로 통일."

write_stub docs/refactoring/README.md "리팩토링 계획·결과 (refactoring)" \
  "리팩토링 계획·진행·결과 기록. \`IMPLEMENTATION_PLAN.md\` (리팩토링 한정) 흡수 대상."

write_stub docs/analysis/README.md "분석 · 리서치 (analysis)" \
  "분석 보고서, 리서치 결과, phase 리포트. \`*_research.md\`, \`*_summary.md\`, \`phase*_report.md\` 흡수 대상."

write_stub docs/test/README.md "테스트 시나리오 · 리포트 (test)" \
  "테스트 계획·시나리오·실행 리포트. \`test_scenarios/\`, \`test_reports/\` 변종 흡수."

write_stub docs/troubleshooting/README.md "문제 해결 (troubleshooting)" \
  "운영 / 디버깅 트러블슈팅 가이드. 단일 \`TROUBLESHOOTING.md\` 는 본 폴더로 승격."

write_stub docs/api/README.md "수동작성 API 참조 (api)" \
  "수동 작성 API 문서. 자동생성 API 는 repo root \`api/\` (Doxygen/Sphinx 빌드 아티팩트) 와 택일 — 한 repo 안에서 한 쪽만 선택."

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
