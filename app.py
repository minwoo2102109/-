import streamlit as st
import datetime
import time
import random

# 1. 페이지 설정
st.set_page_config(page_title="WAKE-UP EFFICACY CENTER", page_icon="🚨", layout="centered")

# 디자인 스타일 적용 (오류 방지를 위해 한 줄씩 처리)
st.markdown("<style>.main { background-color: #0d0d11; color: white; }</style>", unsafe_allow_html=True)
st.markdown("<style>.stMetric { background-color: #16161a; padding: 20px; border-radius: 12px; border: 1px solid #333344; }</style>", unsafe_allow_html=True)
st.markdown("<style>.stMetric label { color: #ffffff !important; font-weight: 700 !important; font-size: 16px !important; }</style>", unsafe_allow_html=True)
st.markdown("<style>div[data-testid='stMetricDelta'] { font-weight: 600 !important; color: #ff3333 !important; }</style>", unsafe_allow_html=True)

# 2. 타이틀 및 상태 배너
st.title("🚨 WAKE-UP CONTROL CENTER")

# 경고 배너 디자인 우회 (단일 따옴표 및 Streamlit 기본 컴포넌트 활용)
st.error("⚠️ ALARM STATUS: ENFORCED | 지옥의 알람이 당신의 아침을 대기 중입니다.")

st.divider()

# 3. 앱 관련 간단 소개 토글 버튼
if 'show_app_intro' not in st.session_state:
    st.session_state.show_app_intro = False

if st.button("📱 이 앱은 무엇인가요? (간단 소개 보기)", use_container_width=True):
    st.session_state.show_app_intro = not st.session_state.show_app_intro

if st.session_state.show_app_intro:
    # 에러가 나던 멀티라인 따옴표를 완전히 제거하고 st.info로 깔끔하게 처리
    st.info("😈 잠결 무의식을 파괴하는 강제 기상 시스템\n\n매일 아침 적응할 수 없는 무작위 소음이 울리며, 잠결에 터치 한 번으로 알람을 끄는 행위를 방지하기 위해 버튼 위치와 슬라이더가 매번 무작위로 셔플됩니다. 마지막으로 화장실로 직접 걸어가 세수한 얼굴을 카메라로 인증해야만 비로소 알람이 종료되는 무자비한 기상 유도 앱입니다.")

st.divider()

# 4. 실효성 증명 데이터 대시보드
st.markdown("<h3 style='color: #ffffff; font-weight: 800; margin-bottom: 15px;'>📊 기상 실효성 보고서</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="🧠 뇌 활성화 지수", value="92%", delta="▲ 15% 전일 대비")
with col2:
    st.metric(label="🧩 평균 미션 해결 시간", value="1분 30초", delta="슬라이더 & 셔플 연계")
with col3:
    st.metric(label="💧 세수 인증 성공률", value="98%", delta="카메라 미션 완료")

st.divider()

# --- 5. 알람 시뮬레이션 및 미션 로직 ---
if 'alarm_triggered' not in st.session_state: st.session_state.alarm_triggered = False
if 'mission_step' not in st.session_state: st.session_state.mission_step = 1
if 'target_slide' not in st.session_state: st.session_state.target_slide = random.randint(6
