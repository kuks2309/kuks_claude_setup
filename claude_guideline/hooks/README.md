# claude_guideline hooks

Claude Code (LLM) 의 SessionStart / PostToolUse / PreToolUse 등의 훅에 등록할 수 있는 보조 스크립트.

## 제공 hook

| 스크립트 | 훅 종류 | 목적 |
|---------|--------|-----|
| [session_start_claude_mistake.sh](session_start_claude_mistake.sh) | SessionStart | `claude-mistake/INDEX.md` 의 §메타 패턴 + §미해결 항목 절을 매 세션 시작에 자동 주입 — 동일 카테고리 재발 차단 |
| [stop_check_abbreviations.py](stop_check_abbreviations.py) | Stop | 응답에 풀어쓰지 않은 약어(JTC·TF·QP 등)가 있으면 Stop 을 차단하고 "원어(한국어 의미, 약어)" 형태로 풀어쓰도록 강제 — 약어 남용 재발 차단 |

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

1. `bash docs/claude_guideline/update.sh` 또는 `install.sh` 로 hooks/ 동기화 (자동 — install.sh 의 FILES 배열에 등록됨).
2. `~/.claude/settings.json` 또는 `<project>/.claude/settings.json` 의 `hooks.SessionStart` 항목에 위 entry 추가.
3. 새 세션 시작 시 stdout 출력이 자동으로 시스템 컨텍스트에 주입됨.

## 설치 — Stop 훅 (`stop_check_abbreviations.py`)

`Stop` 이벤트에 등록한다. 응답 직전 마지막 assistant 메시지를 읽어, 추적 약어가
풀어쓴 키워드 없이 단독으로 쓰였으면 `{"decision":"block"}` 으로 정지를 차단하고
풀어쓰기를 요구한다. `stop_hook_active` 가드로 무한 루프를 막는다.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 docs/claude_guideline/hooks/stop_check_abbreviations.py"
          }
        ]
      }
    ]
  }
}
```

추적 약어 목록은 스크립트 상단의 `ABBREVIATIONS` 배열에서 `(정규식, 풀어쓴 키워드)`
쌍으로 편집한다. 프로젝트별 머신 종속 절대경로가 필요하면 위 `command` 를 절대경로로
바꾸고, 그 설정 파일(`.claude/settings.local.json` 등)은 git 추적에서 제외한다.

## 검증

수동 실행으로 출력 확인:

```bash
bash docs/claude_guideline/hooks/session_start_claude_mistake.sh
```

INDEX.md 가 부재한 워크스페이스에서는 조용히 종료 (exit 0, no output) — 다운스트림 미설치 환경 호환.

`stop_check_abbreviations.py` 는 stdin 으로 `{"transcript_path": ...}` JSON 을 받으므로,
가짜 transcript 한 줄로 차단/통과를 확인할 수 있다:

```bash
printf '{"type":"assistant","message":{"content":[{"type":"text","text":"JTC 토픽으로 전송"}]}}\n' > /tmp/t.jsonl
echo '{"transcript_path":"/tmp/t.jsonl"}' | python3 docs/claude_guideline/hooks/stop_check_abbreviations.py
# -> {"decision": "block", ...}  (약어 JTC 가 풀어쓰기 없이 단독 사용됨)
```

## 신규 hook 추가 시

1. 본 폴더에 `<event>_<purpose>.{sh,py}` 형식으로 추가
2. `chmod +x`
3. 본 README 의 §제공 hook 표에 한 행 추가
4. `install.sh` 의 FILES 배열에 한 줄 추가
5. CHANGELOG 에 entry
