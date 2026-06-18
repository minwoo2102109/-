import streamlit as st
import datetime
import time

# 1. 페이지 기본 설정 및 테마 커스텀
st.set_page_config(
    page_title="얼리버드 웨이크업 (Early Bird Wake-Up)",
    page_icon="☀️",
    layout="centered"
)

# 커스텀 스타일 적용 (아침 감성의 배경과 깔끔한 디자인)
st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom, #1e3c72, #2a5298);
        color: white;
    }
    .stButton>button {
        background-color: #ff9e22 !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 2rem;
    }
    .stButton>button:hover {
        background-color: #e08512 !important;
    }
    .logo-text {
        font-size: 45px !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-text {
        text-align: center;
        color: #f0f0f0;
        font-size: 18px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 로고 및 타이틀 섹션
st.markdown("<p class='logo-text'>☀️ 얼리버드 강제 기상 알람</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-text'>늦잠은 끝! 당신의 활기찬 아침을 강제로 시작합니다.</p>", unsafe_allow_html=True)

st.divider()

# 3. 앱 소개 기능 (버튼 클릭 시 토글)
# Streamlit의 session_state를 활용해 토글 버튼 구현
if 'show_intro' not in session_state:
    st.session_state.show_intro = False

if st.button("📱 앱 소개 보기 / 닫기"):
    st.session_state.show_intro = not st.session_state.show_intro

if st.session_state.show_intro:
    st.info("""
    ### 🔔 얼리버드 강제 기상 앱이란?
    매번 알람을 끄고 다시 자는 분들을 위한 **특단의 조치 프로그램**입니다!
    
    * **강제 미션 수행**: 알람이 울리면 지정된 미션을 해결하기 전까지 알람 소리가 멈추지 않습니다.
    * **스마트 타이머**: 현재 시간과 남은 시간을 실시간으로 확인하며 긴장감을 유지하세요.
    * **아침 루틴 형성**: 미션을 깨며 자연스럽게 뇌를 깨우고 상쾌한 아침을 맞이하세요!
    """)

st.divider()

# 4. 메인 기능: 알람 설정 및 구동
st.subheader("⏰ 알람 설정")

col1, col2 = st.columns(2)
with col1:
    # 현재 시간 표시
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.metric(label="현재 시간", value=current_time)

with col2:
    # 알람 시간 입력 받아오기
    alarm_time = st.time_input("깨어날 시간을 선택하세요", datetime.time(7, 0))

st.write(f"👉 설정된 알람 시간: **{alarm_time.strftime('%H시 %M분')}**")

# 알람 시작 버튼
if st.button("🚀 알람 시스템 가동"):
    st.success(f"🎬 {alarm_time.strftime('%H:%M')}에 강제 기상 알람이 예약되었습니다. 화면을 켜두세요!")
    
    # 배포 환경 테스트를 위한 시뮬레이션 안내문
    st.caption("💡 (테스트 팁: 바로 확인해보려면 현재 시간 1~2분 뒤로 설정해보세요!)")
    
    # 간단한 알람 체크 루프 (실제 서비스 체감용 데모)
    placeholder = st.empty()
    
    while True:
        now = datetime.datetime.now().time()
        # 시/분 단위가 일치하면 알람 발동
        if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
            placeholder.empty()
            st.balloons() # 축하 효과 (시각적 자극)
            
            # 강제 기상 미션 창 등장
            st.error("🚨🚨🚨 위잉위잉! 기상 시간입니다! 🚨🚨🚨")
            st.warning("🔒 [강제 미션] 아래 수학 문제를 풀어야 알람이 종료됩니다!")
            
            # 미션 입력 폼
            with st.form(key='mission_form'):
                answer = st.text_input("퀴즈: 7 x 8 + 15는 무엇일까요?")
                submit_button = st.form_submit_button(label='미션 완료 및 알람 끄기')
                
                if submit_button:
                    if answer == "71":
                        st.success("🎉 미션 성공! 좋은 아침입니다. 오늘도 파이팅!")
                        break
                    else:
                        st.error("❌ 틀렸습니다! 다시 집중해서 풀어보세요!")
            break
            
        # 1초마다 현재 시간 업데이트 체감 주기
        time.sleep(1)
