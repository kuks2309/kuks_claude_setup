#!/usr/bin/env python3
"""PostToolUse hook: reject changelog-style history comments added to code files.

coding.md §수정 이력 기록 forbids comments that narrate modification history
(dates, version tags, old values, "기존/이전" phrasing). History belongs in
docs/code_updates/ and the git commit message; comments state current facts only.

This hook inspects the text ADDED by Edit / Write / MultiEdit calls on code
files. If an added comment line matches a history pattern, it returns
{"decision": "block", "reason": ...} so the model removes the comment and
records the history in code_updates/ instead.

Whitelist: TODO(YYYY-MM-DD) (manual.md format), NOLINT/noqa markers, and
non-code files (.md/.rst/.txt, code_updates/, CHANGELOG, etc.).
Edit PATTERNS / CODE_EXTS below to extend.
"""
import json
import re
import sys

CODE_EXTS = {
    ".c", ".cc", ".cpp", ".cxx", ".h", ".hh", ".hpp", ".ino",
    ".py", ".sh", ".bash", ".js", ".ts", ".tsx", ".jsx",
    ".java", ".kt", ".rs", ".go", ".cs", ".m", ".mm",
    ".cmake", ".yaml", ".yml", ".launch", ".xml", ".msg", ".srv", ".action",
}

SKIP_PATH_PARTS = ("code_updates/", "CHANGELOG", "changelog", "/docs/claude_guideline/hooks/")

# comment marker that starts the comment segment of a line
COMMENT_MARKER = re.compile(r"(//|#|/\*|\*\s|;;|--|<!--)")

# history patterns checked INSIDE the comment segment
PATTERNS = [
    (re.compile(r"\b20\d{2}\s?[-./년]\s?\d{1,2}\s?([-./월]\s?\d{1,2})?"), "날짜"),
    (re.compile(r"\d\s*(→|->)\s*\d"), "값 변천 화살표"),
    (re.compile(r"\bv\d+(\.\d+)*\s*[:—–-]"), "버전 태그"),
    (re.compile(r"기존|이전\s?값|이전에는|원래는?\s|였음|이었음|변경함|변경됨|수정함|수정됨|바꿈"), "이력 서술어"),
]

WHITELIST = re.compile(r"TODO\s*\(|NOLINT|noqa|type:\s*ignore")


def added_texts(tool_name, tool_input):
    if tool_name == "Edit":
        return [tool_input.get("new_string", "")]
    if tool_name == "Write":
        return [tool_input.get("content", "")]
    if tool_name == "MultiEdit":
        return [e.get("new_string", "") for e in tool_input.get("edits", [])]
    return []


def is_code_file(path):
    p = path.replace("\\", "/")
    if any(part in p for part in SKIP_PATH_PARTS):
        return False
    dot = p.rfind(".")
    if dot < 0:
        return False
    return p[dot:].lower() in CODE_EXTS


def scan(text):
    hits = []
    for line in text.splitlines():
        m = COMMENT_MARKER.search(line)
        if not m:
            continue
        comment = line[m.start():]
        if WHITELIST.search(comment):
            continue
        for pat, label in PATTERNS:
            if pat.search(comment):
                hits.append((label, line.strip()))
                break
    return hits


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {}) or {}
    path = tool_input.get("file_path", "") or ""
    if tool_name not in ("Edit", "Write", "MultiEdit") or not is_code_file(path):
        return 0
    hits = []
    for text in added_texts(tool_name, tool_input):
        hits.extend(scan(text))
    if not hits:
        return 0
    shown = "; ".join(f"[{label}] {line[:80]}" for label, line in hits[:3])
    more = f" 외 {len(hits) - 3}건" if len(hits) > 3 else ""
    print(json.dumps({
        "decision": "block",
        "reason": (
            "방금 추가한 주석에 changelog 성 이력이 있습니다 (coding.md §수정 이력 기록 위반): "
            f"{shown}{more}. 해당 주석을 삭제·교정하고 (주석은 현재 코드의 사실만), "
            "이력은 docs/code_updates/ entry 와 git commit message 에 기록하세요. "
            "형식: documentation.md §code_updates 기록 형식."
        ),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
