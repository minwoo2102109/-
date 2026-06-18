import streamlit as st
import datetime
import time
import random

# 1. 페이지 설정
st.set_page_config(page_title="악마의 알람 센터", page_icon="🚨", layout="centered")

# 캐릭터 이미지 URL (이미지 검색 결과 적용)
CHARACTER_URL = "http://googleusercontent.com/image_collection/image_retrieval/14751516888364146340"

# 커스텀 CSS (캐릭터와 다크 테마 강조)
st.markdown(f"""
    <style>
    .main {{ background-color: #0d0d11; color: white; }}
    .stMetric {{ background-color: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; }}
    .char-container {{ text-align: center; margin-bottom: 20px; }}
    .char-img {{ width: 250px; border-radius: 50%; border: 5px solid #ff3333; box-shadow: 0 0 30px #ff3333; }}
    </style>
    """, unsafe_allow_html=True)

# 2. 메인 캐릭터 섹션
st.markdown(f'<div class="char-container"><img src="{CHARACTER_URL}" class="char-img"></div>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #ff3333;'>WAKEY THE GRUDGE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>\"잠들면 내가 찾아갈 거야...\"</p>", unsafe_allow_html=True)

st.divider()

# 3. 오류 수정된 통계 섹션 (delta_color 에러 해결)
st.subheader("📊 당신의 생존 기록")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="이번 주 탈출률", value="92%", delta="4%")
with col2:
    # 에러 원인이었던 delta_color를 안전하게 "normal"로 설정하거나 제거
    st.metric(label="평균 기상 시간", value="1분 24초", delta="-18초", delta_color="normal")
with col3:
    st.metric(label="현재
