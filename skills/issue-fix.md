---
name: issue-fix
description: This skill should be used when the user asks to "fix issue", "fix this error", "이슈 해결", "이슈 기록", pastes an error log or build failure, or when a bug fix is completed and needs recording in issues_and_fixes.md.
---

# Issue Fix Workflow

Automate the full diagnose-fix-record cycle for this ROS2 project. Every fix must produce two documentation updates per CLAUDE.md rules.

## Workflow

### 1. Search Past Issues

Read `docs/issues_fixes/issues_and_fixes.md` (first 200 lines). Grep for keywords from the current error. If a similar past issue exists, reference its root cause as a starting hypothesis.

### 2. Diagnose

Gather evidence before proposing fixes:

- Read the error message completely. Identify the failing node, file, and line.
- Run `grep` for the error string across `src/` to locate the origin.
- Check `git log --oneline -10` and `git diff HEAD~3` for recent changes that may have introduced the regression.
- Form a root-cause hypothesis with file:line evidence.

### 3. Propose Fix

Present the diagnosis to the user before implementing:

- 증상 (symptom): what is observed
- 원인 (root cause): why it happens, citing file:line
- 해결 (proposed fix): minimal change to resolve
- Wait for user approval before proceeding.

### 4. Implement

Apply the approved fix. Follow CLAUDE.md rules:

- One function at a time: read, write, verify.
- Check for duplicate functions/variables before adding new ones.
- For Nav Tool changes, verify both `tm_nav_tool` and `wcs_gui_node.py`.

### 5. Verify

Build the affected package(s):

```bash
cd ~/T-Robot_nav_ros2_ws && colcon build --packages-select <PKG>
```

Run tests if available. Confirm zero build errors before proceeding.

### 6. Record (MANDATORY)

Both files must be updated. Newest entry at top.

**A) `docs/issues_fixes/issues_and_fixes.md`** -- prepend after the `---` separator on line 5:

```
## [YYYY-MM-DD HH:MM] <package> -- <title>

### 증상

### 원인

### 해결책

### 관련 파일
```

**B) `docs/<package>_code_updates.md`** -- prepend under today's date heading:

```
### HH:MM - <7-char hash> / <title>
- **추가|수정|삭제** `<relative path>`
```

Stage all changed files with `git add` (specific files, not `-A`).

## Completion Checklist

- [ ] Root cause identified with file:line
- [ ] User approved the fix before implementation
- [ ] Build passes (`colcon build` exit 0)
- [ ] `issues_and_fixes.md` updated
- [ ] `<pkg>_code_updates.md` updated
- [ ] All modified files staged with `git add`
