#!/bin/bash
# ROS2 tr_driver 통합 테스트 스크립트
# driving_motor_node 실행 상태 및 토픽/서비스 검증

PASS=0; FAIL=0; SKIP=0
NODE_NAME="driving_motor_node"
TIMEOUT_SEC=5

pass() { echo -e "  [PASS] $1"; ((PASS++)); }
fail() { echo -e "  [FAIL] $1"; ((FAIL++)); }
skip() { echo -e "  [SKIP] $1"; ((SKIP++)); }

echo "============================================"
echo " ROS2 tr_driver 통합 테스트"
echo "============================================"

# ROS2 환경 확인
if ! command -v ros2 &>/dev/null; then
    echo "[ERROR] ROS2 환경이 소싱되지 않았습니다."
    echo "  source /opt/ros/\$ROS_DISTRO/setup.bash"
    exit 1
fi

# 1. 노드 실행 확인
echo -e "\n[1] 노드 실행 확인 ($NODE_NAME)"
NODE_LIST=$(ros2 node list 2>/dev/null)
if echo "$NODE_LIST" | grep -q "$NODE_NAME"; then
    pass "$NODE_NAME 실행 중"
else
    fail "$NODE_NAME 미실행"
    echo "  hint: ros2 launch tr_driver driving_motor_launch.py"
    echo "  (노드 미실행 시 이후 테스트는 SKIP 처리됩니다)"
    NODE_RUNNING=false
fi
NODE_RUNNING=${NODE_RUNNING:-true}

# 2. 토픽 리스트 확인
echo -e "\n[2] 토픽 리스트 확인"
EXPECTED_TOPICS=("drives/joint_states" "drives/motor_status" "drives/encoder_raw")
TOPIC_LIST=$(ros2 topic list 2>/dev/null)
for TOPIC in "${EXPECTED_TOPICS[@]}"; do
    if echo "$TOPIC_LIST" | grep -q "$TOPIC"; then
        pass "토픽 존재: /$TOPIC"
    else
        if [ "$NODE_RUNNING" = true ]; then
            fail "토픽 없음: /$TOPIC"
        else
            skip "토픽 확인 불가 (노드 미실행): /$TOPIC"
        fi
    fi
done

# 3. 구독 토픽 확인
echo -e "\n[3] 구독 토픽 확인"
SUB_TOPIC="drives/joint_trajectory"
if echo "$TOPIC_LIST" | grep -q "$SUB_TOPIC"; then
    pass "구독 토픽 존재: /$SUB_TOPIC"
else
    if [ "$NODE_RUNNING" = true ]; then
        fail "구독 토픽 없음: /$SUB_TOPIC"
    else
        skip "구독 토픽 확인 불가 (노드 미실행)"
    fi
fi

# 4. motor_status 토픽 수신 테스트
echo -e "\n[4] motor_status 토픽 수신 테스트"
if [ "$NODE_RUNNING" = true ]; then
    MSG=$(timeout $TIMEOUT_SEC ros2 topic echo /drives/motor_status --once 2>/dev/null)
    if [ -n "$MSG" ]; then
        pass "motor_status 메시지 수신됨"
        echo "$MSG" | head -10 | sed 's/^/  /'
    else
        fail "motor_status 메시지 미수신 (${TIMEOUT_SEC}초)"
    fi
else
    skip "motor_status 수신 불가 (노드 미실행)"
fi

# 5. joint_states 토픽 Hz 확인
echo -e "\n[5] joint_states 퍼블리시 주기 확인"
if [ "$NODE_RUNNING" = true ]; then
    HZ_OUT=$(timeout 5 ros2 topic hz /drives/joint_states --window 5 2>&1 | tail -1)
    if [ -n "$HZ_OUT" ]; then
        pass "joint_states Hz: $HZ_OUT"
    else
        fail "joint_states Hz 측정 실패"
    fi
else
    skip "Hz 확인 불가 (노드 미실행)"
fi

# 6. joint_trajectory 명령 발행 테스트 (속도 0으로 안전 테스트)
echo -e "\n[6] joint_trajectory 명령 발행 (속도 0 - 안전 테스트)"
if [ "$NODE_RUNNING" = true ]; then
    ros2 topic pub --once /drives/joint_trajectory \
        trajectory_msgs/msg/JointTrajectory \
        "{joint_names: ['wheel_left', 'wheel_right'],
          points: [{velocities: [0.0, 0.0],
                    time_from_start: {sec: 0, nanosec: 100000000}}]}" \
        2>/dev/null
    if [ $? -eq 0 ]; then
        pass "joint_trajectory 발행 완료 (속도 0)"
    else
        fail "joint_trajectory 발행 실패"
    fi
else
    skip "명령 발행 불가 (노드 미실행)"
fi

# 7. 노드 파라미터 확인
echo -e "\n[7] 노드 파라미터 확인"
if [ "$NODE_RUNNING" = true ]; then
    PARAMS=$(ros2 param list /$NODE_NAME 2>/dev/null)
    if [ -n "$PARAMS" ]; then
        pass "파라미터 조회 성공"
        for P in can_interface motor_freq num_driver gear_ratio; do
            if echo "$PARAMS" | grep -q "$P"; then
                VAL=$(ros2 param get /$NODE_NAME $P 2>/dev/null)
                echo "  $P = $VAL"
            fi
        done
    else
        fail "파라미터 조회 실패"
    fi
else
    skip "파라미터 확인 불가 (노드 미실행)"
fi

echo -e "\n============================================"
echo " 결과: PASS=$PASS / FAIL=$FAIL / SKIP=$SKIP"
echo "============================================"
[ $FAIL -eq 0 ] && exit 0 || exit 1
