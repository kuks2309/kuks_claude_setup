#!/bin/bash
# RoboteQ CANOpen 단위 테스트 스크립트
# CANOpen DS301/DS402 기반 CAN 통신 검증
# Node ID: 1 (Heartbeat:0x701, TPDO1:0x181, RPDO1:0x201, SDO TX:0x581, SDO RX:0x601)

CAN_IF="${1:-can0}"
NODE_ID=1
PASS=0; FAIL=0; SKIP=0

pass() { echo -e "  [PASS] $1"; ((PASS++)); }
fail() { echo -e "  [FAIL] $1"; ((FAIL++)); }
skip() { echo -e "  [SKIP] $1"; ((SKIP++)); }

echo "============================================"
echo " RoboteQ CAN 단위 테스트 (인터페이스: $CAN_IF)"
echo "============================================"

# 1. CAN 인터페이스 확인
echo -e "\n[1] CAN 인터페이스 확인"
if ip link show "$CAN_IF" 2>/dev/null | grep -q "UP"; then
    pass "$CAN_IF UP 상태"
else
    fail "$CAN_IF 인터페이스 없거나 DOWN 상태"
    echo "  hint: sudo ip link set $CAN_IF up type can bitrate 500000"
fi
# TX/RX 에러 카운터
if command -v ip &>/dev/null; then
    ERR=$(ip -d -s link show "$CAN_IF" 2>/dev/null | grep -i "errors")
    if [ -n "$ERR" ]; then
        echo "  에러 상태: $ERR"
    fi
fi

# 2. Heartbeat 수신 (0x701)
echo -e "\n[2] Heartbeat 수신 확인 (0x701)"
if command -v candump &>/dev/null; then
    HB=$(timeout 3 candump "$CAN_IF",701:7FF -n 1 2>/dev/null)
    if [ -n "$HB" ]; then
        pass "Heartbeat 수신: $HB"
        STATE=$(echo "$HB" | awk '{print $NF}')
        case "$STATE" in
            00) echo "  상태: Boot-up" ;;
            04) echo "  상태: Stopped" ;;
            05) echo "  상태: Operational" ;;
            7F) echo "  상태: Pre-Operational" ;;
            *)  echo "  상태: Unknown (0x$STATE)" ;;
        esac
    else
        fail "Heartbeat 미수신 (3초 타임아웃)"
    fi
else
    skip "can-utils 미설치 (sudo apt install can-utils)"
fi

# 3. NMT Start 전송
echo -e "\n[3] NMT Start 전송 (000#01.01)"
if command -v cansend &>/dev/null; then
    cansend "$CAN_IF" "000#01$(printf '%02X' $NODE_ID)" 2>/dev/null
    if [ $? -eq 0 ]; then
        pass "NMT Start Remote Node 전송 완료 (Node $NODE_ID)"
    else
        fail "NMT Start 전송 실패"
    fi
else
    skip "cansend 미설치"
fi

# 4. TPDO1 수신 확인 (0x181)
echo -e "\n[4] TPDO1 수신 확인 (0x181)"
if command -v candump &>/dev/null; then
    TPDO=$(timeout 3 candump "$CAN_IF",181:7FF -n 1 2>/dev/null)
    if [ -n "$TPDO" ]; then
        pass "TPDO1 수신: $TPDO"
    else
        fail "TPDO1 미수신 (3초 타임아웃, NMT Operational 상태 필요)"
    fi
else
    skip "candump 미설치"
fi

# 5. SDO 읽기 - Device Type (0x1000)
echo -e "\n[5] SDO 읽기 - Device Type (0x1000:00)"
if command -v cansend &>/dev/null && command -v candump &>/dev/null; then
    # SDO Upload Request: 40 00 10 00 00 00 00 00
    candump "$CAN_IF",581:7FF -n 1 -T 3000 &>/tmp/sdo_resp.txt &
    DUMP_PID=$!
    sleep 0.1
    cansend "$CAN_IF" "601#4000100000000000" 2>/dev/null
    wait $DUMP_PID 2>/dev/null
    SDO_RESP=$(cat /tmp/sdo_resp.txt 2>/dev/null)
    if [ -n "$SDO_RESP" ]; then
        pass "SDO 응답 (Device Type): $SDO_RESP"
    else
        fail "SDO 응답 없음"
    fi
    rm -f /tmp/sdo_resp.txt
else
    skip "can-utils 미설치"
fi

# 6. SDO 읽기 - Manufacturer Device Name (0x1008)
echo -e "\n[6] SDO 읽기 - Manufacturer Device Name (0x1008:00)"
if command -v cansend &>/dev/null && command -v candump &>/dev/null; then
    candump "$CAN_IF",581:7FF -n 1 -T 3000 &>/tmp/sdo_resp2.txt &
    DUMP_PID=$!
    sleep 0.1
    cansend "$CAN_IF" "601#4008100000000000" 2>/dev/null
    wait $DUMP_PID 2>/dev/null
    SDO_RESP2=$(cat /tmp/sdo_resp2.txt 2>/dev/null)
    if [ -n "$SDO_RESP2" ]; then
        pass "SDO 응답 (Manufacturer): $SDO_RESP2"
    else
        fail "SDO 응답 없음"
    fi
    rm -f /tmp/sdo_resp2.txt
else
    skip "can-utils 미설치"
fi

# 7. CAN 에러 카운터 확인
echo -e "\n[7] CAN 에러 카운터 확인"
CAN_STATE=$(ip -d link show "$CAN_IF" 2>/dev/null | grep "can state")
if [ -n "$CAN_STATE" ]; then
    echo "  $CAN_STATE"
    if echo "$CAN_STATE" | grep -q "ERROR-ACTIVE"; then
        pass "CAN 버스 정상 (ERROR-ACTIVE)"
    elif echo "$CAN_STATE" | grep -q "ERROR-PASSIVE"; then
        fail "CAN 버스 경고 (ERROR-PASSIVE)"
    elif echo "$CAN_STATE" | grep -q "BUS-OFF"; then
        fail "CAN 버스 오류 (BUS-OFF)"
    else
        pass "CAN 상태 확인됨"
    fi
else
    skip "CAN 상태 정보 없음"
fi

# 8. Heartbeat 주기 측정
echo -e "\n[8] Heartbeat 주기 측정"
if command -v candump &>/dev/null; then
    HB_LOG=$(timeout 5 candump "$CAN_IF",701:7FF -t a -n 5 2>/dev/null)
    if [ -n "$HB_LOG" ]; then
        TIMES=$(echo "$HB_LOG" | awk '{gsub(/[()]/, "", $1); print $1}')
        PREV=""
        INTERVALS=""
        for T in $TIMES; do
            if [ -n "$PREV" ]; then
                DIFF=$(echo "$T - $PREV" | bc 2>/dev/null)
                [ -n "$DIFF" ] && INTERVALS="$INTERVALS $DIFF"
            fi
            PREV=$T
        done
        if [ -n "$INTERVALS" ]; then
            AVG=$(echo "$INTERVALS" | tr ' ' '\n' | awk '{s+=$1;n++} END{if(n>0) printf "%.0f", s/n*1000}')
            pass "Heartbeat 평균 주기: ${AVG}ms (${#INTERVALS// /+} 샘플)"
        else
            pass "Heartbeat 수신됨 (주기 계산 불가 - bc 미설치)"
        fi
    else
        fail "Heartbeat 미수신 (5초)"
    fi
else
    skip "candump 미설치"
fi

echo -e "\n============================================"
echo " 결과: PASS=$PASS / FAIL=$FAIL / SKIP=$SKIP"
echo "============================================"
[ $FAIL -eq 0 ] && exit 0 || exit 1
