#!/usr/bin/env python3
"""Stop hook: block ending a turn that edited code without reflecting records.

coding.md mandates the cycle: read module docs -> modify code -> reflect the
modification into docs/code_updates/ (history entry) and architecture/
inventory.md (function/global-variable tables). This hook enforces the record
half at every response completion (Stop fires per turn, NOT at session end).

Scan of the CURRENT turn (transcript entries after the last genuine user text
message): if a code file inside a guideline-adopting project (ancestor dir has
docs/claude_guideline/) was Edited/Written but no code_updates/ file nor any
inventory.md was Edited/Written in the same turn, the stop is blocked once
(stop_hook_active guard) with instructions to reflect the records first.
"""
import json
import os
import sys

CODE_EXTS = {
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".ino",
    ".py", ".sh", ".bash", ".js", ".ts", ".tsx", ".jsx",
    ".java", ".kt", ".rs", ".go", ".cs", ".m", ".mm",
    ".cmake", ".yaml", ".yml", ".launch", ".xml", ".msg", ".srv", ".action",
}

SKIP_PATH_PARTS = ("/docs/", "code_updates/", "/hooks/", "/.claude/", "/scratchpad/")


def is_code_file(path):
    p = path.replace("\\", "/")
    if any(part in p for part in SKIP_PATH_PARTS):
        return False
    return os.path.splitext(p)[1].lower() in CODE_EXTS


def in_adopting_project(file_path):
    """Walk up to the repo boundary (.git) only — a nested repo without its own
    docs/claude_guideline/ is NOT adopting, even inside an adopting workspace."""
    d = os.path.dirname(os.path.abspath(file_path))
    while True:
        if os.path.isdir(os.path.join(d, "docs", "claude_guideline")):
            return True
        if os.path.exists(os.path.join(d, ".git")):
            return False
        parent = os.path.dirname(d)
        if parent == d:
            return False
        d = parent


def is_record_path(path):
    p = path.replace("\\", "/")
    return "code_updates/" in p or p.endswith("inventory.md")


def current_turn_tool_uses(transcript_path):
    """tool_use items after the last genuine user text message.

    Denied/errored calls (their tool_result carries is_error) are excluded —
    a PreToolUse-denied Write appears in the transcript as tool_use but never
    modified any file, so counting it would be a false positive."""
    try:
        with open(transcript_path, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception:
        return []
    last_user = -1
    parsed = []
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except Exception:
            parsed.append(None)
            continue
        parsed.append(obj)
        if obj.get("type") == "user" or obj.get("role") == "user":
            msg = obj.get("message", obj)
            content = msg.get("content", "")
            if isinstance(content, str) and content.strip():
                last_user = i
            elif isinstance(content, list):
                has_text = any(isinstance(c, dict) and c.get("type") == "text"
                               for c in content)
                has_result = any(isinstance(c, dict) and c.get("type") == "tool_result"
                                 for c in content)
                if has_text and not has_result:
                    last_user = i
    uses = []
    error_ids = set()
    for obj in parsed[last_user + 1:]:
        if not obj:
            continue
        msg = obj.get("message", obj)
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for c in content:
            if not isinstance(c, dict):
                continue
            if c.get("type") == "tool_use":
                uses.append(c)
            elif c.get("type") == "tool_result" and c.get("is_error"):
                error_ids.add(c.get("tool_use_id"))
    return [u for u in uses if u.get("id") not in error_ids]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("stop_hook_active"):
        return 0
    uses = current_turn_tool_uses(data.get("transcript_path", ""))
    code_edits, record_writes = [], []
    for u in uses:
        if u.get("name") not in ("Edit", "Write", "MultiEdit"):
            continue
        p = (u.get("input") or {}).get("file_path", "") or ""
        if not p:
            continue
        if is_record_path(p):
            record_writes.append(p)
        elif is_code_file(p) and in_adopting_project(p):
            code_edits.append(p)
    if not code_edits or record_writes:
        return 0
    shown = ", ".join(sorted(set(code_edits))[:5])
    print(json.dumps({
        "decision": "block",
        "reason": (
            "이번 턴에 코드를 수정했지만 기록 반영이 없습니다 (coding.md 수정전 읽기·"
            "수정후 기록 사이클): " + shown + ". 마치기 전에 ① 해당 모듈 docs/code_updates/ 에 "
            "수정 이력 entry 를 작성하고 (형식: documentation.md §code_updates 기록 형식), "
            "② 함수/전역 변수의 추가·삭제·시그니처 변경 또는 미등재 파일이면 "
            "architecture/inventory.md 표를 갱신하세요 (없으면 수정 파일 범위만큼 생성)."
        ),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
