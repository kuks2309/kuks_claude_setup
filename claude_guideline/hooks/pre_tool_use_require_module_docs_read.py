#!/usr/bin/env python3
"""PreToolUse hook: require reading module docs BEFORE editing code.

coding.md §함수·전역 변수 인벤토리 갱신 mandates: before modifying code, read the
module's inventory (architecture/inventory.md) and recent code_updates/ entries.
This hook enforces the read half of the read->modify->record cycle.

On Edit/Write/MultiEdit targeting a code file inside a guideline-adopting
project (an ancestor directory contains docs/claude_guideline/), it scans the
session transcript for a prior Read (or Edit/Write) of that module's
inventory.md / any code_updates/ file. If the docs exist but were never read
this session, the tool call is denied with instructions to read them first.

If the module has no inventory yet, the edit is allowed — creation is enforced
by the Stop-side hook (stop_check_code_record_reflected.py).
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
    ext = os.path.splitext(p)[1].lower()
    return ext in CODE_EXTS


def find_module_docs(file_path):
    """Walk up from the edited file: nearest docs/architecture/inventory.md and
    docs/code_updates/. Stop at (and require) a guideline-adopting project root."""
    d = os.path.dirname(os.path.abspath(file_path))
    inventory, code_updates, adopting = None, None, False
    while True:
        inv = os.path.join(d, "docs", "architecture", "inventory.md")
        cu = os.path.join(d, "docs", "code_updates")
        if inventory is None and os.path.isfile(inv):
            inventory = inv
        if code_updates is None and os.path.isdir(cu) and os.listdir(cu):
            code_updates = cu
        if os.path.isdir(os.path.join(d, "docs", "claude_guideline")):
            adopting = True
            break
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return adopting, inventory, code_updates


def session_touched_paths(transcript_path):
    """All file paths this session has Read / Edited / Written."""
    touched = set()
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                msg = obj.get("message", obj)
                content = msg.get("content")
                if not isinstance(content, list):
                    continue
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "tool_use" and \
                            c.get("name") in ("Read", "Edit", "Write", "MultiEdit"):
                        p = (c.get("input") or {}).get("file_path")
                        if p:
                            touched.add(os.path.abspath(p))
    except Exception:
        pass
    return touched


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") not in ("Edit", "Write", "MultiEdit"):
        return 0
    path = (data.get("tool_input") or {}).get("file_path", "") or ""
    if not path or not is_code_file(path):
        return 0
    adopting, inventory, code_updates = find_module_docs(path)
    if not adopting:
        return 0
    touched = session_touched_paths(data.get("transcript_path", ""))
    missing = []
    if inventory and os.path.abspath(inventory) not in touched:
        missing.append(inventory)
    if code_updates and not any(t.startswith(os.path.abspath(code_updates) + os.sep)
                                for t in touched):
        missing.append(code_updates + "/ (최근 entry 1개)")
    if not missing:
        return 0
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "코드 수정 전 모듈 기록을 먼저 읽어야 합니다 (coding.md §함수·전역 변수 "
                "인벤토리 갱신 — 수정 전 읽기 의무). 아직 읽지 않음: "
                + "; ".join(missing)
                + ". Read 로 읽은 뒤 이 수정을 다시 시도하세요."
            ),
        }
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
