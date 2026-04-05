---
name: capture-test
description: 화면 캡처 후 Claude가 기능 테스트 결과를 분석하는 스킬
user_invocable: true
trigger: capture-test
arguments:
  - name: description
    description: 분석할 내용 또는 확인할 사항 (선택)
    required: false
---

# Screen Capture & Analysis Skill

화면을 캡처하고 Claude가 기능 동작 여부를 분석합니다.

## Instructions

사용자가 `/capture-test`를 호출하면 다음 단계를 수행하세요:

### Step 1: 캡처 모드 확인
사용자에게 캡처 모드를 질문합니다 (인자로 지정하지 않은 경우):
- **active** (기본값): 현재 활성 윈도우 캡처
- **full**: 전체 화면 캡처
- **region**: 특정 영역 캡처 (좌표 필요)

빠른 실행을 원하면 기본값(active)으로 바로 진행합니다.

### Step 2: 화면 캡처 실행
Python 스크립트를 실행하여 캡처합니다:

```bash
"/c/Program Files/Python313/python.exe" ~/.claude/tools/capture_screen.py --project "{현재 프로젝트 경로}" --mode {active|full|region}
```

- Linux 환경에서는 `python3` 명령을 사용합니다.
- 캡처된 파일은 `{프로젝트}/screenshot/YYYYMMDD_HHMMSS.png`에 저장됩니다.

### Step 3: 캡처 이미지 분석
Read 도구로 캡처된 이미지를 읽고 다음을 분석합니다:

1. **UI 요소 확인**: 윈도우, 버튼, 메뉴, 탭 등이 정상 표시되는지
2. **에러 확인**: 에러 메시지, 팝업, 크래시 화면 유무
3. **기능 동작 확인**: 사용자가 설명한 기능이 정상 동작하는지
4. **레이아웃 확인**: UI 요소 배치가 올바른지

### Step 4: 분석 결과 보고
다음 형식으로 보고합니다:

```
## 캡처 분석 결과

**캡처 파일**: screenshot/YYYYMMDD_HHMMSS.png
**캡처 모드**: active/full/region

### 확인 항목
- [ ] UI 정상 표시
- [ ] 에러 없음
- [ ] 기능 동작 정상
- [ ] 레이아웃 정상

### 상세 분석
(이미지에서 확인된 내용 상세 기술)

### 발견된 문제
(문제가 있으면 기술, 없으면 "발견된 문제 없음")
```

### 참고
- 사용자가 특정 확인 사항을 인자로 전달하면 해당 항목을 중점적으로 분석합니다.
- 문제 발견 시 `docs/issues_and_fixes/` 폴더에 이슈를 기록합니다.
