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

# 커스텀 스타일 적용 (어두운 블랙 & 테크니컬 레드 조합으로 관제 센터 느낌 강조)
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
    /* 경고 배너 애니메이션 효과 */
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

# 3. 실시간 시스템 감시 상태 배너 (기상 예약 창 대신 들어간 메인 비주얼)
st.markdown("""
    <div class="warning-banner">
        <h2 style="color: #ff3333; margin: 0; font-weight: 900;">⚠️ ALARM STATUS: ENFORCED</h2>
        <p style="color: #ffffff; margin: 8px 0 0 0; font-size: 16px;">
            내일 아침 시스템이 강제로 가동됩니다. 백그라운드 우회 및 탈출 시도는 불가능합니다.
        </p>
    </div>
""", unsafe_allow_html=True)

# 4. 앱 정체성 키워드 소개 (버튼 토글)
if 'show_intro' not in st.session_state:
    st.session_state.show_intro = False

if st.button("📱 이 시스템의 절대 탈출 불가능 메커니즘 보기", use_container_width=True):
    st.session_state.show_intro = not st.session_state.show_intro

if st.session_state.show_intro:
    st.info("""
    ### 🛑 잠결 뇌세포를 강제로 깨우는 3단계 장치
    
    * **⚡ 예측 불허 무작위 소음**: 매일 아침 칠판 긁는 소리, 실제 전원 대피령 등 상상하지도 못한 괴기한 소리가 무작위로 울려 뇌가 소음에 적응할 틈을 주지 않습니다.
