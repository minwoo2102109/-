import streamlit as st
import datetime
import time
import random

# 1. 페이지 기본 설정 및 테마 커스텀
st.set_page_config(
    page_title="악마의 강제 기상 알람",
    page_icon="🚨",
    layout="centered"
)

# 커스텀 스타일 적용 (경각심을 주는 붉은 톤과 어두운 배경 조합)
st.markdown("""
    <style>
    .main {
        background-color: #111116;
        color: #ffffff;
    }
    .stButton>button {
        font-weight: bold;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        background-color: #ff3333 !important;
        color: white !important;
        border: none;
    }
    .stButton>button:hover {
        background-color: #cc0000 !important;
    }
    .logo-text {
        font-size: 40px !important;
        font-weight: 900;
        text-align: center;
        color: #ff3333;
        margin-bottom: 0px;
    }
    .sub-text {
        text-align: center;
        color: #aaaaaa;
        font-size: 16px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 로고 및 타이틀 섹션
st.markdown("<p class='logo-text'>🚨 악마의 무작위 기상 알람</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>적응 불가능한 소음과 랜덤 미션, 세수 인증까지 완료해야 꺼집니다.</p>", unsafe_allow_html=True)

st.divider()

# 3. 앱 소개 기능 (버튼 클릭 시 토글)
if 'show_intro' not in st.session_state:
    st.session_state.show_intro = False

if st.button("📱 이 지옥 같은 알람의 작동 원리 보기", use_container_width=True):
    st.session_state.show_intro = not st.session_state.show_intro

if st.session_state.show_intro:
    st.info("""
    ### 🛑 절대 잠결에 끌 수 없는 악마의 알람!
    
    * **⚡ 예측 불허 무작위 소음**: 매일 아침 칠판 긁는 소리, 전원 대피령 등 상상하지도 못한 괴기한 소리가 무작위로 울려 뇌가 소음에 적응할 틈을 주지 않습니다.
    * **🎮 랜덤 UI 셔플 게임**: 잠결에 무의식적으로 알람을 끄는 것을 막기 위해, 해제 버튼의 위치와 슬라이더의 목표 방향이 매번 게임처럼 무작위로 변경됩니다.
    * **🌊 최종 세수 카메라 인증**: 침대에서 완전히 벗어나 화장실로 이동한 뒤, 물기 촉촉한 얼굴이나 욕실을 카메라로 직접 촬영해 인증해야 비로소 지옥의 알람이 종료됩니다.
    """)

st.divider()

# 4. 메인 기능: 알람 설정 및 구동 세션 상태 초기화
st.subheader("⏰ 기상 시간 예약")
col1, col2 = st.columns(2)
with col1:
    st.metric(label="현재 시간", value=datetime.datetime.now().strftime("%H:%M:%S"))
with col2:
    alarm_time = st.time_input("절대 깨야 하는 시간", datetime.time(7, 0))

# 알람 및 미션 관련 세션 상태 관리
if 'alarm_triggered' not in st.session_state:
    st.session_state.alarm_triggered = False
if 'mission_step' not in st.session_state:
    st.session_state.mission_step = 1 # 1: 랜덤게임, 2: 세수인증, 3: 완료
if 'random_sound' not in st.session_state:
    st.session_state.random_sound = ""
if 'btn_pos' not in st.session_state:
    st.session_state.btn_pos = random.randint(0, 2) # 0: 왼쪽, 1: 중앙, 2: 오른쪽
if 'target_slide' not in st.session_state:
    st.session_state.target_slide = random.randint(60, 95)

# 가상 구동 버튼
if st.button("🔥 지옥의 알람 모드 가동", use_container_width=True):
    st.session_state.alarm_triggered = True
    st.session_state.mission_step = 1
    
    # 무작위 사운드 리스트 셔플
    sounds = [
        "🔊 [🚨삐이익-!! 전원 대피령 실제 상황경보 소음]가 폭발합니다!",
        "🔊 [🐓 미친 듯이 목청 터지는 시골 장닭 소리]가 귀를 찢습니다!",
        "🔊 [💥 콰과광! 칠판 긁는 소리와 싱크홀 폭발음 조합]이 반복됩니다!",
        "🔊 [📢 이봐!! 일어나!! 지금 안 일어나면 인생 망해!! 잔소리 랩] 재생 중!"
    ]
    st.session_state.random_sound = random.choice(sounds)
    st.rerun()

# --- 5. 알람 발동 및 미션 레이아웃 ---
if st.session_state.alarm_triggered:
    st.error(st.session_state.random_sound)
    
    # [1단계 미션]: 랜덤 UI 셔플 게임
    if st.session_state.mission_step == 1:
        st.warning(f"🔒 [1단계 미션] 잠결 조작 방지! 슬라이더를 정확히 **{st.session_state.target_slide}**에 맞추고 해제 버튼을 누르세요!")
        
        user_slide = st.slider("정밀 슬라이더 제어", 0, 100, 0)
        
        # 버튼 위치 무작위 배치를 위한 컬럼 생성
        b_col1, b_col2, b_col3 = st.columns(3)
        
        # 매번 무작위 컬럼에 버튼 배치
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
                # 실패 시 버튼 위치와 슬라이더 목표값 다시 재셔플
                st.session_state.btn_pos = random.randint(0, 2)
                st.session_state.target_slide = random.randint(60, 95)
                st.rerun()

    # [2단계 미션]: 아침 세수 인증 (카메라)
    elif st.session_state.mission_step == 2:
        st.info("🌊 [2단계 최종 미션] 화장실로 가서 세수한 물기 촉촉한 얼굴(또는 욕실)을 카메라로 비춰 인증하세요!")
        
        # Streamlit 내장 카메라 입력 기능 호출
        img_file = st.camera_input("정신 차리기용 세수 인증샷 촬영")
        
        if img_file is not None:
            st.success("✅ 인증 사진 확인 완료! 지옥의 알람이 종료되었습니다.")
            st.session_state.mission_step = 3
            st.session_state.alarm_triggered = False # 알람 종료
            st.balloons()
            st.rerun()
            
# 최종 완료 화면
if st.session_state.mission_step == 3:
    st.success("🎉 완벽하게 깨어나셨군요! 상쾌하고 활기찬 하루를 시작하세요!")
    if st.button("🔄 알람 다시 대기하기", use_container_width=True):
        st.session_state.mission_step = 1
        st.rerun()
