import streamlit as st
import time
from datetime import datetime
import json
import urllib.request
import base64

# 기본 페이지 설정
st.set_page_config(page_title="세수 알람", page_icon="🧼", layout="centered")

def play_sound(sound_type):
    """HTML5 오디오를 활용하여 브라우저 강제 효과음 재생"""
    urls = {
        "alarm": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
        "success": "https://actions.google.com/sounds/v1/cheering/applause_yeehaw.ogg",
        "fail": "https://actions.google.com/sounds/v1/cartoon/slide_whistle_down.ogg"
    }
    url = urls.get(sound_type)
    if url:
        loop = "loop" if sound_type == "alarm" else ""
        html = f'<audio autoplay {loop} style="display:none;"><source src="{url}" type="audio/ogg"></audio>'
        st.components.v1.html(html, height=0)

def verify_wash_face_api(image_bytes):
    """라이브러리 의존성 없는 순수 HTTP 방식의 Gemini API 요청"""
    if "GEMINI_API_KEY" not in st.secrets:
        return False, "Secrets 설정에서 API 키를 확인해주세요."
    
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"
