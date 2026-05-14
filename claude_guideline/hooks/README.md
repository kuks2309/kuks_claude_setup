# claude_guideline hooks

Claude Code (LLM / Large Language Model) 의 SessionStart / PostToolUse / PreToolUse 등의 훅에 등록할 수 있는 보조 스크립트.

## 제공 hook

| 스크립트 | 훅 종류 | 목적 |
|---------|--------|-----|
| [session_start_claude_mistake.sh](session_start_claude_mistake.sh) | SessionStart | `claude-mistake/INDEX.md` 의 §메타 패턴 + §미해결 항목 절을 매 세션 시작에 자동 주입 — 동일 카테고리 재발 차단 |

## 설치 — `~/.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "bash docs/claude_guideline/hooks/session_start_claude_mistake.sh"
      }
    ]
  }
}
```

다운스트림 프로젝트에서:

1. `bash docs/claude_guideline/update.sh` 또는 `install.sh` 로 `hooks/` 동기화 (자동 — `install.sh` 의 FILES 배열에 등록됨).
2. `~/.claude/settings.json` 또는 `<project>/.claude/settings.json` 의 `hooks.SessionStart` 항목에 위 entry 추가.
3. 새 세션 시작 시 stdout 출력이 자동으로 시스템 컨텍스트에 주입됨.

## 검증

수동 실행으로 출력 확인:

```bash
bash docs/claude_guideline/hooks/session_start_claude_mistake.sh
```

`INDEX.md` 가 부재한 워크스페이스에서는 조용히 종료 (`exit 0`, no output) — 다운스트림 미설치 환경 호환.

## 자동화 정책 합치

본 hook 은 [skill_update.md](../skill_update.md) §자동화 정책 의 **자동 인용 (passive cite)** 트리거 — `claude-mistake/INDEX.md` 의 문서 내용만 컨텍스트에 주입하며, 어떤 파일 생성·commit·다운로드도 수행하지 않는다.

## 신규 hook 추가 시

1. 본 폴더에 `<event>_<purpose>.sh` 형식으로 추가
2. `chmod +x`
3. 본 README 의 §제공 hook 표에 한 행 추가
4. `install.sh` 의 FILES 배열에 한 줄 추가
5. CHANGELOG 에 entry
6. [skill_update.md](../skill_update.md) §자동화 정책 의 4 표현 중 어느 것에 해당하는지 본문에 명시
