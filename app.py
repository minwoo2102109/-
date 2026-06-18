import streamlit as st
import datetime
import time
import random

# 1. 페이지 설정
st.set_page_config(page_title="WAKE-UP EFFICACY CENTER", page_icon="🚨", layout="centered")

# 디자인 스타일 적용 (글씨 선명도 대폭 강화)
st.markdown("""
    <style>
    .main { background-color: #0d0d11; color: white; }
    
    /* 대시보드 카드 스타일 */
    .stMetric { 
        background-color: #16161a; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #333344;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    
    /* [핵심 수정] 흐릿한 라벨 글씨를 완전히 선명한 흰색으로 변경 */
    .stMetric label { 
        color: #ffffff !important; 
        font-weight: 700 !important; 
        font-size: 16px !important;
        opacity: 1 !important;
    }
    
    /* 대시보드 큰 숫자(Value) 스타일 강화 */
    .stMetric .st-enter {
        font-weight: 800 !important;
    }
    
    /* 하단 서브 텍스트(Delta) 색상 강조 */
    .stMetric div[data-testid="stMetricDelta"] {
        font-weight: 600 !important;
        color: #ff3333 !important;
    }

    .warning-banner {
        background: linear-gradient(45deg, #330000, #110000);
        border: 2px solid #ff3333; padding: 20px; border-radius: 15px; text-align: center;
        margin-bottom: 25px;
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
    <div class
