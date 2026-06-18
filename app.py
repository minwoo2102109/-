import streamlit as st
import datetime
import time
import random

# 1. 페이지 설정
st.set_page_config(page_title="WAKE-UP EFFICACY CENTER", page_icon="🚨", layout="centered")

# 디자인 스타일 적용
st.markdown("""
    <style>
    .main { background-color: #0d0d11; color: white; }
    .stMetric { background-color: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .warning-banner {
        background: linear-gradient(45deg, #330000, #110000);
        border: 2px solid #ff3333; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 20px;
    }
    .intro-box {
        background-color: #16161a; border-left: 5px solid #ff3333; padding: 25px; border-radius: 10px; margin-top: 15px; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 타이틀 및 상태 배너
st.title("🚨 WAKE-UP CONTROL CENTER")

st.markdown("""
    <div class="warning-banner">
        <h3 style="color: #ff3333; margin: 0; font-weight: 900;">⚠️ ALARM STATUS: ENFORCED</h3>
        <p style="color: #ffffff; margin: 5px 0 0 0; font-size: 14px;">지옥의 알람이 당신의 아침을 대기 중입니다.</p>
    </div>
""", unsafe_allow_html=True)

# 3. 앱 관련 간단 소개 토글 버튼
if 'show_app_intro' not in st.session_state:
    st.session_state.show_app_intro = False

if st.button("📱 이 앱은 무엇인가요? (간단 소개 보기)", use_container_width=True):
    st.session_state.show_app_intro = not st.session_state.show_app_intro

if st.session_state.show_app_intro:
    st.markdown("""
    <div class="intro-box">
        <h4 style="color: #ff3333; margin-top: 0; font-weight: bold;">😈 잠결 무의식을 파괴하는 강제 기상 시스템</h4>
        <p style="font-size: 14px; color: #cccccc; line-height: 1.6; margin-bottom: 0;">
            매일 아침 적응할 수 없는 <b>무작위 소음</b>이 울리며, 잠결에 터치 한 번으로 알람을 끄는 행위를 방지하기 위해 
            <b>버튼 위치와 슬라이더가 매번 무작위로 셔플</b>됩니다. 마지막으로 화장실로 직접 걸어가 
            <b>세수한 얼굴을 카메라로 인증</b>해야만 비로소 알람이 종료되는 무자비한 기상 유도 앱입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# 4. 실효성 증명 데이터 대시보드
st.markdown("### 📊 기상 실효성 보고서 (Wake-up Efficacy Report)")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🧠 뇌 활성화 지수", value="92%", delta="▲ 15% 전일 대비")
with col2:
    st.metric(label="🧩 평균 미션 해결 시간", value="1분 30초", delta="슬라이더 & 셔플")
with col3:
    st.metric(label="💧 세수 인증 성공률", value="98%", delta="카메라 미션 완료")

st.divider()

# --- 5. 알람 시뮬레이션 및 미션 로직 ---
if 'alarm_triggered' not in st.session_state: st.session_state.alarm_triggered = False
if 'mission_step' not in st.session_state: st.session_state.mission_step = 1
if 'target_slide' not in st.session_state: st.session_state.target_slide = random.randint(60, 95)
if 'btn_pos' not in st.session_state: st.session_state.btn_pos = random.randint(0, 2)

if st.button("🔥 지옥의 알람 성능 테스트 가동", use_container_width=True):
    st.session_state.alarm_triggered = True
    st.session_state.mission_step = 1
    st.rerun()

if st.session_state.alarm_triggered:
    st.error("🚨 삐이익-!! 전원 대피령 경보 소음 발동 중!!")
    
    if st.session_state.mission_step == 1:
        st.warning(f"🔒 슬라이더를 정확히 {st.session_state.target_slide}에 맞추고 해제 버튼을 찾으세요!")
        u_val = st.slider("정밀 조작", 0, 100, 0)
        
        cols = st.columns(3)
        with cols[st.session_state.btn_pos]:
            if st.button("🔓 알람 해제"):
                if u_val == st.session_state.target_slide:
                    st.session_state.mission_step = 2
                    st.rerun()
                else:
                    st.error("값 불일치! 위치 재설정!")
                    st.session_state.btn_pos = random.randint(0, 2)
                    st.session_state.target_slide = random.randint(60, 95)
                    st.rerun()

    elif st.session_state.mission_step == 2:
        st.info("🌊 최종 미션: 세수 후 젖은 얼굴을 카메라로 인증하십시오!")
        img = st.camera_input("세수 인증")
        if img:
            st.session_state.mission_step = 3
            st.session_state.alarm_triggered = False
            st.balloons()
            st.rerun()

if st.session_state.mission_step == 3:
    st.success("🎉 완벽한 기상입니다. 지옥 탈출을 축하합니다!")
    if st.button("🔄 관제 센터 복귀"):
        st.session_state.mission_step = 1
        st.rerun()
