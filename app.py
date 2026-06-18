import streamlit as st
import datetime
import time
import random

# 1. 페이지 설정 및 테마 커스텀
st.set_page_config(
    page_title="WAKE-UP CONTROL CENTER",
    page_icon="🚨",
    layout="centered"
)

# AI가 생성해준 알람 로봇 캐릭터 이미지 URL
CHAR_URL = "https://images.unsplash.com/photo-1596464716127-f2a82984de30?auto=format&fit=crop&w=500&q=80"

st.markdown("""
    <style>
    .main { background-color: #0d0d11; color: #ffffff; }
    .stButton>button {
        font-weight: bold; border-radius: 12px; padding: 0.8rem 2rem;
        background-color: #ff3333 !important; color: white !important; border: none;
        box-shadow: 0 4px 15px rgba(255, 51, 51, 0.4);
    }
    .stButton>button:hover {
        background-color: #cc0000 !important; box-shadow: 0 4px 25px rgba(255, 51, 51, 0.6);
    }
    .warning-banner {
        background: linear-gradient(45deg, #220000, #440000); border: 2px solid #ff3333;
        padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 메인 캐릭터 및 타이틀 레이아웃
st.image(CHAR_URL, caption="WAKEY ALARM BOT v1.0", width=300)
st.title("🚨 WAKE-UP CONTROL CENTER")

# 3. 실시간 시스템 감시 상태 배너
st.markdown("""
    <div class="warning-banner">
        <h3 style="color: #ff3333; margin: 0; font-weight: 900;">⚠️ ALARM STATUS: ACTIVE</h3>
        <p style="color: #ffffff; margin: 5px 0 0 0; font-size: 14px;">시스템 가동 중. 우회 및 탈출 불가능.</p>
    </div>
""", unsafe_allow_html=True)

# 4. 앱 정체성 키워드 소개 (오류 방지를 위해 온전한 한 줄 처리)
if 'show_intro' not in st.session_state:
    st.session_state.show_intro = False

if st.button("📱 탈출 불가능 메커니즘 확인", use_container_width=True):
    st.session_state.show_intro = not st.session_state.show_intro

if st.session_state.show_intro:
    st.markdown("### 🛑 3단계 강제 기상 장치")
    st.write("⚡ **예측 불허 무작위 소음**: 매일 아침 상상하지도 못한 괴기한 소리가 무작위로 울려 적응할 틈을 주지 않습니다.")
    st.write("🎮 **랜덤 UI 셔플 게임**: 잠결 무의식 종료를 막기 위해 버튼 위치와 슬라이더 목표치가 매번 바뀝니다.")
    st.write("🌊 **최종 세수 카메라 인증**: 화장실로 이동해 물기 촉촉한 얼굴이나 욕실을 촬영해야 알람이 꺼집니다.")

st.divider()

# 5. 나의 기상 기록 통계 (안전한 delta_color 적용 및 한글 짧게 처리)
st.subheader("📊 탈출 리포트")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="이번 주 성공률", value="92%", delta="4%")
with col2:
    st.metric(label="평균 소요 시간", value="1분 24초", delta="-18초")
with col3:
    st.metric(label="현재 연승 기록", value="7일 연속", delta="🔥")

st.divider()

# 6. 오늘의 무작위 소음 예측 섹션
st.subheader("🔮 내일 아침 공포 예측")
st.warning("내일 아침 배정 주파수: [칠판 긁는 소리] 또는 [고출력 장닭 사운드] 무작위 매칭 예정.")

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

if st.button("🔥 악마의 알람 즉시 테스트 가동", use_container_width=True):
    st.session_state.alarm_triggered = True
    st.session_state.mission_step = 1
    
    sounds = [
        "🔊 [🚨삐이익-!! 전원 대피령 경보 소음] 발동!",
        "🔊 [🐓 목청 터지는 시골 장닭 소리] 발동!",
        "🔊 [💥 칠판 긁는 소리와 싱크홀 폭발음] 발동!",
        "🔊 [📢 지금 안 일어나면 인생 망하는 잔소리 랩] 발동!"
    ]
    st.session_state.random_sound = random.choice(sounds)
    st.rerun()

# 알람 발동 레이아웃
if st.session_state.alarm_triggered:
    st.error(st.session_state.random_sound)
    
    # [1단계 미션]
    if st.session_state.mission_step == 1:
        st.warning(f"🔒 슬라이더를 정확히 {st.session_state.target_slide}에 맞추고 해제 버튼을 누르세요!")
        user_slide = st.slider("정밀 조작", 0, 100, 0)
        
        b_col1, b_col2, b_col3 = st.columns(3)
        if st.session_state.btn_pos == 0:
            with b_col1: btn = st.button("🔓 알람 해제")
        elif st.session_state.btn_pos == 1:
            with b_col2: btn = st.button("🔓 알람 해제")
        else:
            with b_col3: btn = st.button("🔓 알람 해제")
            
        if 'btn' in locals() and btn:
            if user_slide == st.session_state.target_slide:
                st.session_state.mission_step = 2
                st.rerun()
            else:
                st.session_state.btn_pos = random.randint(0, 2)
                st.session_state.target_slide = random.randint(60, 95)
                st.rerun()

    # [2단계 미션]
    elif st.session_state.mission_step == 2:
        st.info("🌊 화장실에서 세수한 물기 촉촉한 얼굴을 카메라로 인증하세요!")
        img_file = st.camera_input("세수 인증샷 촬영")
        
        if img_file is not None:
            st.session_state.mission_step = 3
            st.session_state.alarm_triggered = False
            st.balloons()
            st.rerun()
            
# 최종 완료 화면
if st.session_state.mission_step == 3:
    st.success("🎉 탈출 성공! 활기찬 하루를 시작하세요!")
    if st.button("🔄 관제 센터 복귀", use_container_width=True):
        st.session_state.mission_step = 1
        st.rerun()
