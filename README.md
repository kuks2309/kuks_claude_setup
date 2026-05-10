# kuks_claude_setup

Claude Code 프로젝트를 위한 고도화된 작업 지침(SOP)과 한국 실무 환경(ROS2, 임베디드, HWP/PPTX)에 최적화된 자동화 스킬 모음.

> Korean-first specialist setup for Claude Code, ROS2, and Korean Business Automation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.7.0-blue.svg)](claude_guideline/VERSION)

---

## 프로젝트 구조

| 디렉토리 | 설명 |
| :--- | :--- |
| [`claude_guideline/`](claude_guideline/) | 핵심 작업 지침 (SSOT). Coding, GitHub, ROS2, 기술 부채 방지 등 메타 규칙 |
| [`skills/`](skills/) | Claude 자동화 스킬 (.md 기반). 단위 테스트, 작업 로그, 이슈 해결 |
| [`agents/`](agents/) | 도메인 전문 에이전트 지침 (예: RoboteQ 모터 컨트롤러) |
| [`hwp스킬/`](hwp%EC%8A%A4%ED%82%AC/) | 아래 한글(HWP/HWPX) 구조 분석 및 자동화 처리 스킬 |
| [`pptx-design-styles/`](pptx-design-styles/) | PowerPoint 디자인 스타일 가이드 및 레이아웃 자동화 자산 |
| [`tools/`](tools/) | 화면 캡처, Git 훅, 하드웨어 유틸리티 등 지원 도구 |
| [`conversation_backup/`](conversation_backup/) | Claude Code 대화 백업 도구 |
| [`project-autolearn/`](project-autolearn/) | 커밋 단위 도구 사용 패턴 자동 학습 시스템 |

## 빠른 설치

대상 프로젝트 루트(=`.git` 보유 디렉토리)에서 다음 명령 실행:

```bash
bash <(curl -sSL https://raw.githubusercontent.com/kuks2309/kuks_claude_setup/master/claude_guideline/install.sh)
```

`docs/claude_guideline/` 에 가이드라인 자산이 설치됩니다. 이후 워크스페이스 루트의 `CLAUDE.md` "문서 작업 규칙" 섹션에서 진입 링크를 추가하거나 [`templates/CLAUDE.md.template`](claude_guideline/templates/CLAUDE.md.template) 을 참고해 새 `CLAUDE.md` 를 작성합니다.

## Mental Model

본 저장소의 자산은 세 계층으로 관리됩니다:

1. **Guidelines (메타 규칙)** — Claude가 어떻게 사고하고 행동해야 하는지 정의하는 SOP·룰. SSOT 단일 근원 원칙으로 관리.
2. **Skills (자동화)** — 특정 반복 작업을 표준화한 `.md` 기반 스킬 (단위 테스트, worklog, 이슈 수정 등).
3. **Agents (도메인 전문가)** — 특정 하드웨어/도메인 지식을 부여하는 전문 페르소나.

상세 작업 규칙은 [`claude_guideline/README.md`](claude_guideline/README.md) 진입점 표를 따라 진입합니다.

## 핵심 진입점

| 영역 | 파일 |
| :--- | :--- |
| 사용자 지시 처리 9단계 SOP | [`claude_guideline/user_instruction_handling_sop.md`](claude_guideline/user_instruction_handling_sop.md) |
| 코드 작업 규칙 | [`claude_guideline/coding.md`](claude_guideline/coding.md) |
| GitHub 워크플로 | [`claude_guideline/github.md`](claude_guideline/github.md) |
| 매뉴얼/데이터시트 인용·검증 | [`claude_guideline/manual.md`](claude_guideline/manual.md) |
| ROS2/임베디드 작업 규칙 | [`claude_guideline/ros2.md`](claude_guideline/ros2.md) |

## 업데이트

설치 후 가이드라인 갱신은 다음 명령으로 수행합니다:

```bash
bash docs/claude_guideline/update.sh           # 대화식
bash docs/claude_guideline/update.sh --auto    # 자동 (patch/minor)
```

`docs/claude_guideline/local/` 폴더의 프로젝트 고유 override 는 업데이트 시 보존됩니다.

---

## English Summary

**kuks_claude_setup** is a curated collection of guidelines and automated skills designed for **Claude Code**. It provides a professional-grade software engineering environment, specifically tailored for Korean developers working with ROS2, embedded systems, and local business automation.

The core asset is `claude_guideline/`, a Single Source of Truth (SSOT) defining Standard Operating Procedures (SOPs) for request handling, coding standards, GitHub workflows, and manual/datasheet citation. These rules guide Claude through deterministic, evidence-driven engineering work, preventing iteration anti-patterns and unfounded claims.

The repository also includes specialized skills for HWPX automation, PPTX design styles, and hardware-specific agents (e.g., RoboteQ motor controllers). It is built with a "Korean-first" mindset while maintaining global engineering standards. Documentation is primarily in Korean; English summary and per-file English sections are added incrementally.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
