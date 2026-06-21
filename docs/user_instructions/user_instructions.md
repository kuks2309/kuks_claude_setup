# User Instructions

본 파일은 사용자 원문 보존 — 요약 / 해석 / 재구성 금지. KST 시각 + 시간 역순 (최신 위, prepend).

---

## 2026-06-21 (KST) — 다중 원격 저장소 동기 정책 SSOT (remote_push_policy.md) 신설 + CLAUDE.md 진입표 등록

> "푸쉬는 kuks2309라 fito에 둘다 올리는거 알죠?"

> "https://github.com/kuks2309/kuks_claude_agent_setup"

> "https://github.com/FitoControl/FITO_claude_skill_install"

> "kuks_claude_agent_setup 이 /home/amap/Project/claude_code/kuks_claude_skill_setup과 관련이 있는데"

> "그리고 /home/amap/Project/claude_code/kuks_claude_skill_setup을 피토에 넣어야 하고"

> "이 것에 대한 규칙을 만들어주세요."

> "claude.md도 넣어야 하지 않는지?"

> "기록 커밋 푸쉬"

---

## 2026-06-21 (KST) — ROS2 인터페이스 감사 SOP 후속 합의 3 (Timer/Thread 룰) 등록 + docs/followups 파일 갱신

> "합의사항은 기록하고 다음 세션에서 진행할 수 있도록 해주세요."

> "세셔 ㄴ정리할까요?"

> "ROS2에서  timer, thread 등에 대한 규약이 있는지?"

> "등록 부탁"

> "먼저 기록"

---

## 2026-06-13 (KST) — docs/ 49 entry × D1+D5 분류 매트릭스 (14명 팀) — Step 2 embedding 학습 코퍼스 목적

> "현재 프로젝트에서 docs폴더를 분석해서 사용자의 요구 내용을 찾아서 분류가 가능한지? /team 20명 최대 투입"

> "다시 질문"

> "진행"

> "이 목적이 뭘까?  Step2에서 사용자의 의도를  그 동안 프로젝트를 통하여 분류하기 위한 것인데"

> "사용자의 요청사항을 분류하기 위해서 embedding 에 사용하기 위한것"

> "기록하고 세션 정리를 위해서 커밋 푸쉬"

---

## 2026-06-13 (KST) — user_instruction_recording.md PWM-VV 배포 실패 진단 + α 옵션 2 ("지시용 — 기록 금지") 적용

> "C:\Temp\PWM-VV\docs\claude_guideline\user_instruction_recording_live_v2.md 에 왜 기록  C:\Temp\PWM-VV\docs\user_instructions 에 기록해야 하는데
>
> 다른 프로젝트에 적용하니 이렇게 문제가 생기는데 지침이 이상한것 아닌지?"

> "지시 폴더 guide_line과 실제 적는 폴더를 명확하게 구분되어 잇는데 지시를 잘못한거지"

> "개새기 같이 지시를 해서아 시팔 정말 열받네"

> "user_instruction_recording.md 는 합의해서 만든 것인데 지금와서 무슨 개소리야"

> "제목 바로 아래 1 줄 추가: \"기록 대상은 docs/user_instructions/user_instructions.md — 본 파일에는 기록 금지.\"  이렇게 해서 알겟니?"

> "정말 짜증나네 이거 하느데 2일이나 소요하나개새기야"

> "본 파일은 지시용으로 기록금지 이렇게 해야 명확하지 않을가/"

> "좀 잘하자"

> "2"

> "기록하고 세션 정리를 위해서 커밋 푸쉬"

---

## 2026-05-25 (KST) — ROS2 인터페이스 감사 SOP §8 신설·확장 + docs 브랜치 분리 워크플로

> "ros2 도메인의 경우 토픽 엑션 등의 리스트를 만들어서 문서화하고 qos준수를 확인해야 합니다.
> 각 노드의 토픽 리스트등을 작성해야 하죠.
>
> 이를 위해서 토픽에 대해서 분석한 문서를 이 컴퓨터에서 조사하고 정규화할 수 잇는 지시 문서를 만들어주세요"

> "오케이... kuks_claude_setup_new 에 업데이트 부탁"

> "진행"

> "깃 허브 연동/"

> "분석 테이블에는
> 파일(노드), 토픽명 , 기능 ,설명 등이 포함되는 테이블을 만들어야 하는데 반영이 되엇나요?
>
> 나머지 서비도 마찬가지
>
> 그리고 토픽을 중심으로 어던 노드들이 연결되고 역활에 대한 테이블 생성 지시도 되엇는지?"

> "진행"

> "깃 허브에 싱크 부탁"

> "/home/amap/Project/claude_code/kuks_claude_setup_new 에 문서 업데이트 하거나 추가하고. 깃은  다른 브렌치에 올릴 것"

> "qos 매칭 문서는 별로도 생성하는 것이 어덜까?"

> "tf_frame, service에 대한 문서도 작성하면 좋을 것 같은데 지시서에 추가 가능할까??"

> "진행"

> "tf에 관한 내용도 포함되어 잇는지?  rviz2는개발시에는 src 폴더에 위치
> 항상 폴더 관련은 재 배포를 고려해서 패키지 상대 폴더 위치로 정의할 것
> 이 내용 포함인지?"

> "rviz2에서 config를 바굴 경우 scr폴더에서 실행하지 않고 install 에서 실행하면 수정할떄 불폄하다는 이야기임
> 그래서  src 폴더에 rviz config를 두어야 함"

> "그리고 rqt_graph를 저장해서 토픽간의 연결을 볼 수 있도록 해야 함"

> "세션 정리를 위해서 기록 커밋 푸쉬"

---

## 2026-05-22 (KST) — external_reference_handling.md SSOT 신설 + v2 마이그레이션 Step 1-3

> "폴더 /home/amap/Study/ros2_3dslam_ws/docs 를 참조해서 manual.md 분석 부탁"

> "우리 새로운 /home/amap/Project/claude_code/kuks_claude_setup_new 에 적용하기 위해서 개선될 내용은?"

> "독립적으로 작동하게 .. 현재는 신규 생성이 다 독립적으로 수행이 가능하도록 작성하는데"

> "현재 모든 파일은 독립 SSOT 으로 ㅈ가성중입니다."

> "사용자가 \"QoS 원칙 추가\" 별도 언급 → 사례와 원칙이 같은 §에서 강화됨 <- 이건 코딩으로
> manual.md는 관련 도메인의 문서를 참조하는 것이아닌지?"

> "파일 이름부터가 직관적이지 못함"

> "A"

> "도메인에 따라서 다양한 manual이 존재 할 수 있으므로 이에 대한 보완이 필요함"

> "opencv 도 포함"

> "1"

> "a"

> "왜 omc skill ?"

> "진행 해줏ㅅ"

> "commit / push 는 별도 명시 승인"

> "커밋푸쉬"

> "커밋푸쉬  kuks_claude_setup_new/ 의 내용을 깃 커밋해야 함"

> "기존 것을  /home/amap/Project/claude_code/kuks_claude_setup_new로 교체하는 작업이니 이에 적합하도록 설정"

> "전부다 순서적으로 진행할 것"

> "완료 가 모두 되엇으면 세션 종료 진행하기 위햐서 기록, 깃 커밋 푸쉬 부탁"

---
