import streamlit as st
import datetime
import time
import random

# 1. 페이지 기본 설정 및 테마 커스텀
st.set_page_config(
    page_title="악마의 강제 기상 알람 센터",
    page_icon="🚨",
    layout="centered"
)

# 커스텀 스타일 적용 (어두운 블랙 & 테크니컬 레드 조합)
st.markdown("""
    <style>
    .main {
        background-color: #0d0d11;
        color: #ffffff;
    }
    .stButton>button {
        font-weight: bold;
        border-radius: 12px;
        padding: 0.8rem 2rem;
        background-color: #ff3333 !important;
        color: white !important;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 51, 51, 0.4);
    }
    .stButton>button:hover {
        background-color: #cc0000 !important;
        box-shadow: 0 4px 25px rgba(255, 51, 51, 0.6);
    }
    .logo-text {
        font-size: 42px !important;
        font-weight: 900;
        text-align: center;
        color: #ff3333;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }
    .sub-text {
        text-align: center;
        color: #888888;
        font-size: 15px;
        margin-bottom: 25px;
    }
    .warning-banner {
        background: linear-gradient(45deg, #220000, #440000);
        border: 2px solid #ff3333;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 10px #ff3333; }
        50% { box-shadow: 0 0 25px #ff3333; }
        100% { box-shadow: 0 0 10px #ff3333; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 로고 및 타이틀 섹션
st.markdown("<p class='logo-text'>🚨 WAKE-UP CONTROL CENTER</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>악마의 무작위 기상 시스템 메인 관제 탑</p>", unsafe_allow_html=True)

# 3. 실시간 시스템 감시 상태 배너
st.markdown("""
    <div class="warning-banner">
        <h2 style="color: #ff3333; margin: 0; font-weight: 900;">⚠️ ALARM STATUS: ENFORCED</h2>
        <p style="color: #ffffff; margin: 8px 0 0 0; font-size: 16px;">
            내일 아침 시스템이 강제로 가동됩니다. 백그라운드 우회 및 탈출 시도는 불가능합니다.
        </p>
    </div>
""", unsafe_allow_html=True)

# 4. 앱 정체성 키워드 소개
if 'show_intro' not in st.session_state:
    st.session_state.show_intro = False

if st.button("📱 이 시스템의 절대 탈출 불가능 메커니즘 보기", use_container_width=True):
    st.session_state.show_intro = not st.session_state.show_intro

if st.session_state.show_intro:
    st.markdown("### 🛑 잠결 뇌세포를 강제로 깨우는 3단계 장치")
    st.write("⚡ **예측 불허 무작위 소음**: 매일 아침 칠판 긁는 소리, 실제 전원 대피령 등 상상하지도 못한 괴기한 소리가 무작위로 울려 뇌가 소음에 적응할 틈을 주지 않습니다.")
    st.write("🎮 **랜덤 UI 셔플 게임**: 잠결에 무의식적으로 알람을 터치해 끄 것을 막기 위해, 해제 버튼의 위치와 슬라이더의 목표값이 매번 게임처럼 무작위로 변경됩니다.")
    st.write("🌊 **최종 세수 카메라 인증**: 침대에서 완전히 벗어나 화장실로 이동한 뒤, 물기 촉촉한 얼굴이나 욕실을 카메라로 직접 촬영해 인증해야 비로소 지옥의 알람이 종료됩니다.")

st.divider()

# 5. 나의 기상 기록 통계 (오류 수정: delta_color를 최신 스펙인 "inverse_trending"으로 변경)
st.subheader("📊 지옥 탈출 실시간 리포트")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="이번 주 기상 성공률", value="92%", delta="▲ 4%")
with col2:
    st.metric(label="평균 탈출 소요 시간", value="1분 24초", delta="-18초 (단축)", delta_color="inverse_trending")
with col3:
    st.metric(label="현재 갱신 중인 연승", value="7일 연속", delta="🔥")

st.divider()

# 6. 오늘의 무작위 소음 예측 섹션
st.subheader("🔮 내일 아침의 공포 예측")
st.markdown("""
    <div style="background-color: #16161a; padding: 15px; border-radius: 10px; border-left: 5px solid #ff9900;">
        <span style="color: #ff9900; font-weight: bold;">[시스템 경고]</span> 내일 아침 배정된 소음 주파수 유형은 <b>'칠판 긁는 소리 계열'</b> 또는 <b>'고출력 장닭 사운드'</b> 중 하나로 무작위 매칭되었습니다. 마음의 준비를 하십시오.
    </div>
""", unsafe_allow_html=True)

st.divider()

# --- 7. 알람 시뮬레이션 구동 및 미션 로직 ---
if 'alarm_triggered' not in st.session_state:
    st.session_state.alarm_triggered = False
if 'mission_step' not in st.session_state:
    st.session_state.mission_step = 1
if 'random_sound' not in st.session_state:
    st.session_state.random_sound = ""
if 'btn_pos' not in st.session_state:
    st.session_state.btn_pos = random.randint(0, 2)
if 'target_slide' not in st.session_state:
    st.session_state.target_slide = random.randint(60, 95)

st.markdown("<p style='text-align: center; color: #888aa0;'>⚠️ 다른 페이지로 넘어가기 전, 시스템이 제대로 작동하는지 지금 테스트해보세요.</p>", unsafe_allow_html=True)
if st.button("🔥 악마의 알람 즉시 테스트 가동", use_container_width=True):
    st.session_state.alarm_triggered = True
    st.session_state.mission_step = 1
    
    sounds = [
        "🔊 [🚨삐이익-!! 전원 대피령 실제 상황경보 소음]가 폭발합니다!",
        "🔊 [🐓 미친 듯이 목청 터지는 시골 장닭 소리]가 귀를 찢습니다!",
        "🔊 [💥 콰과광! 칠판 긁는 소리와 싱크홀 폭발음 조합]이 반복됩니다!",
        "🔊 [📢 이봐!! 일어나!! 지금 안 일어나면 인생 망해!! 잔소리 랩] 재생 중!"
    ]
    st.session_state.random_sound = random.choice(sounds)
    st.rerun()

# 알람 발동 레이아웃
if st.session_state.alarm_triggered:
    st.error(st.session_state.random_sound)
    
    # [1단계 미션]: 랜덤 UI 셔플 게임
    if st.session_state.mission_step == 1:
        st.warning(f"🔒 [1단계 미션] 잠결 조작 방지! 슬라이더를 정확히 {st.session_state.target_slide}에 맞추고 해제 버튼을 누르세요!")
        
        user_slide = st.slider("정밀 슬라이더 제어", 0, 100, 0)
        
        b_col1, b_col2, b_col3 = st.columns(3)
        if st.session_state.btn_pos == 0:
            with b_col1: btn = st.button("🔓 알람 해제 시도")
        elif st.session_state.btn_pos == 1:
            with b_col2: btn = st.button("🔓 알람 해제 시도")
        else:
            with b_col3: btn = st.button("🔓 알람 해제 시도")
            
        if 'btn' in locals() and btn:
            if user_slide == st.session_state.target_slide:
                st.success("잠결 조작 통과! 최종 단계로 이동합니다.")
                st.session_state.mission_step = 2
                st.rerun()
            else:
                st.error(f"실패! 정확히 {st.session_state.target_slide}에 맞춰야 합니다. 현재 값: {user_slide}")
                st.session_state.btn_pos = random.randint(0, 2)
                st.session_state.target_slide = random.randint(60, 95)
                st.rerun()

    # [2단계 미션]: 아침 세수 인증 (카메라)
    elif st.session_state.mission_step == 2:
        st.info("🌊 [2단계 최종 미션] 화장실로 가서 세수한 물기 촉촉한 얼굴(또는 욕실)을 카메라로 비춰 인증하세요!")
        img_file = st.camera_input("정신 차리기용 세수 인증샷 촬영")
        
        if img_file is not None:
            st.success("✅ 인증 사진 확인 완료! 지옥의 알람이 종료되었습니다.")
            st.session_state.mission_step = 3
            st.session_state.alarm_triggered = False
            st.balloons()
            st.rerun()
            
# 최종 완료 화면
if st.session_state.mission_step == 3:
    st.success("🎉 완벽하게 깨어나셨군요! 상쾌하고 활기찬 하루를 시작하세요!")
    if st.button("🔄 관제 센터 대기 화면으로 복귀", use_container_width=True):
        st.session_state.mission_step = 1
        st.rerun()
