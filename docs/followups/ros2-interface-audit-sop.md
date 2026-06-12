# Follow-ups: ROS2 인터페이스 감사 SOP

- **브랜치**: `docs/ros2-interface-audit-sop`
- **대상 파일**: `claude_guideline/coding/ros2.md`
- **사용자 verbatim 근거**: `docs/user_instructions/user_instructions.md` 의 2026-05-25 entry

§8 본문(8.1~8.8) 은 `06558c7` → `9d1f0f0` → `31e87e8` 으로 push 완료. 본 문서는 같은 세션(2026-05-25)에서 합의됐으나 본문에 반영되지 않은 후속 항목을 추적한다. 구현 완료 시 해당 항목을 본 문서에서 체크 표시 또는 제거하고 동일 브랜치에 commit.

다음 세션은 본 문서를 진입점으로 사용한다.

---

## [ ] 합의 1 — §3.9 설정 파일 / 패키지 경로 (재배포)

§3 추가 룰의 신규 절. 3 하위 항목.

### §3.9.1 설정 파일 src 원본 수정

- 모든 설정 파일(rviz·yaml·json·urdf·xacro) 은 `src/<pkg>/...` 원본 편집
- `install/share/<pkg>/...` 사본 직접 수정 시 `colcon build` 가 src→install 복사로 덮어써 변경 사항이 사라짐
- `--symlink-install` 옵션 디폴트 사용 — install/share 가 src 의 symlink 가 되어 install 경로 접근에도 실제 수정은 src 에 반영 (Linux/macOS)

### §3.9.2 rviz2 config 특화 (★ GUI 저장 함정)

- rviz2 메뉴 "Save Config" / `Ctrl+S` 는 **launch 시 가리킨 파일 경로에 그대로 덮어쓴다**
- 그 경로가 `install/share/.../X.rviz` 이고 `--symlink-install` 도 아니면 → 다음 `colcon build` 에서 작업이 모두 사라진다
- 그러므로 rviz2 config 는 항상 **src 에 보관**하고, 다음 둘 중 하나로 launch:
  1. `--symlink-install` 디폴트 + `get_package_share_directory()` (★ 권장 — 패키지 상대 경로 유지하면서 src 가 실질적 저장 대상)
  2. symlink 미지원 환경에선 launch 에서 src 절대 경로 직접 지정
- 일반 yaml 은 IDE 로 수정하므로 위 함정이 없지만, rviz2 는 GUI 가 저장 주체라 별도 명시

### §3.9.3 패키지 상대 경로 (재배포)

- 코드·launch·config 에서 절대 경로 하드코드 금지, 패키지 상대 경로 API 사용:
  - C++: `ament_index_cpp::get_package_share_directory("<pkg>")`
  - Python: `ament_index_python.packages.get_package_share_directory`
  - launch.py: `os.path.join(get_package_share_directory('<pkg>'), 'config', 'X.yaml')`
  - launch.xml: `$(find-pkg-share <pkg>)/config/X.yaml`
  - URDF/xacro: `$(find <pkg>)/...`
- 이유: 배포·다른 호스트 설치 시 절대 경로는 깨진다

### 연관 보완

- **§4 A 체크리스트** 3 항목 추가:
  - "설정 파일 install/share 직접 수정 없음 (§3.9.1)"
  - "rviz config src 보관 + launch 경로 정합 (§3.9.2)"
  - "절대 경로 → 패키지 상대 경로 치환 완료 (§3.9.3)"
- **§5 평가 태그** `[path]` 추가 — 절대 경로 / install/share 직접 참조 / rviz2 저장 경로
- **§7 자체 점검 grep** 추가:
  - 절대 경로 패턴 — `grep -nE '"/(home|opt|root|usr/local)/[^"]+"' src/**/*.{py,yaml,launch.py,rviz,xml}`
  - install/share 직접 참조 — `grep -nE 'install/share/[a-z_]+' src/**/*.{py,launch.py,xml}`

---

## [ ] 합의 2 — rqt_graph 산출물 추가

§8 감사 SOP 에 토픽 간 연결 시각화 산출물 추가. §8.6.1 토픽 연결 맵(표)의 **시각 동반**.

- **§8.3.2 P3 런타임 실측 명령** 에 추가:

  ```bash
  rqt_graph                     # GUI 에서 노드/토픽 그래프 → File > Save As PNG/SVG
  ```

- **§8.2 산출물 위치** 표에 한 줄 추가:

  | 토픽 그래프 시각화 | `docs/rqt_graph.png` (또는 `.svg`) | rqt_graph GUI 캡처 — §8.6.1 토픽 연결 맵 시각 보조 |

- **§8.8 B 체크리스트** 추가:
  - "rqt_graph 캡처 `docs/rqt_graph.png` 가 §8.6.1 토픽 연결 맵과 정합 (노드·토픽 수 일치)"

---

## 다음 세션 진입 순서

1. `git -C kuks_claude_setup checkout docs/ros2-interface-audit-sop`
2. 본 문서 읽기 — 합의 사항 확인 (project memory `project_pending_ros2_audit_followups` 과 동일 내용)
3. `kuks_claude_setup_new/claude_guideline/coding/ros2.md` 편집:
   - §3.9 신설 (§3.8 micro-ROS 뒤에 추가)
   - §8.2 산출물 표·§8.3.2 P3 명령·§8.8 B 체크리스트 보강 (rqt_graph)
   - §4 A 체크리스트·§5 평가 태그·§7 grep 보강 (§3.9 연관 보완)
4. repo 로 cp → `git add claude_guideline/coding/ros2.md` 단일 파일 → commit (`feat(claude_guideline):` prefix) → push
5. 본 문서의 해당 체크박스 표시 또는 제거 → `git add docs/followups/ros2-interface-audit-sop.md` → commit → push
6. 두 합의 모두 완료되면 본 문서 삭제 + 메모리 갱신
