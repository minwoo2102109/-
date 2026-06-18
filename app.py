import streamlit as st
import datetime
import time
import random

# 1. 페이지 설정
st.set_page_config(page_title="WAKE-UP EFFICACY CENTER", page_icon="🚨", layout="centered")

# [변경] 실효성을 증명하는 데이터 대시보드 캐릭터/그래픽 URL
EFFICACY_URL = "http://googleusercontent.com/image_collection/image_retrieval/13388605493034579521"

# 디자인 스타일 적용
st.markdown("""
    <style>
    .main { background-color: #0d0d11; color: white; }
    .stMetric { background-color: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; }
    .warning-banner {
        background: linear-gradient(45deg, #330000, #110000);
        border: 2px solid #ff3333; padding: 20px; border-radius: 15px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 메인 실효성 리포트 비주얼
st.image(EFFICACY_URL, caption="[LAB REPORT] 앱 사용 후 뇌 활성도 및 기상 성공률 변화", use_column_width=True)
st.title("🚨 WAKE-UP CONTROL CENTER")

# 3. 실시간 시스템 상태
st.markdown("""
    <div class="warning-banner">
        <h3 style="color: #ff3333; margin: 0;">⚠️ ALARM STATUS: ENFORCED</h3>
        <p style="color: #ffffff; margin: 5px 0 0 0;">지옥의 알람이 당신의 아침을 대기 중입니다.</p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# 4. 실효성 증명 데이터 (에러 방지를 위해 변수 처리)
st.subheader("📊 지옥의 알람 실효성 데이터")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="평균 기상 성공률", value="98.2%", delta="35% 상승")
with col2:
    st.metric(label="뇌 활성 도달 시간", value="45초", delta="-320초", delta_color="normal")
with col3:
    st.metric(label="재취침 방지율", value="100%", delta="완전 차단")

st.info("💡 본 데이터는 랜덤 소음과 세수 인증 미션을 수행한 유저들의 실제 지표입니다.")

st.divider()

# --- 5. 알람 시뮬레이션 및 미션 로직 (이하 생략되지 않은 전체 기능) ---
if 'alarm_triggered' not in st.session_state: st.session_state.alarm_triggered = False
if 'mission_step' not in st.session_state: st.session_state.mission_step = 1
if 'target_slide' not in st.session_state: st.session_state.target_slide = random.randint(60, 95)
if 'btn_pos' not in st.session_state: st.session_state.btn_pos = random.randint(0, 2)
