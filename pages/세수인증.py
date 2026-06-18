import streamlit as st
import time
from datetime import datetime
from google import genai
from google.genai import types
from google.genai.errors import APIError
import random

# 페이지 레이아웃 및 테마 설정
st.set_page_config(page_title="폭풍 기상 알람", page_icon="🚨", layout="centered")

# --- 🔊 엄청난 소리 무한 재생 및 효과음 함수 ---
def play_sound(sound_type):
    """HTML5 오디오를 사용해 절대 꺼지지 않는 강력한 사이렌과 소리 효과 제공"""
    # 더 자극적이고 엄청난 사이렌 소리 주소로 배치
    sound_urls = {
        "alarm": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
        "success": "https://actions.google.com/sounds/v1/cheering/applause_yeehaw.ogg",
        "fail": "https://actions.google.com/sounds/v1/cartoon/slide_whistle_down.ogg"
    }
    url = sound_urls.get(sound_type)
    if url:
        loop_attr = "loop" if sound_type == "alarm" else ""
        audio_html = f'<audio autoplay {loop_attr} style="display:none;"><source src="{url}" type="audio/ogg"></audio>'
        st.components.v1.html(audio_html, height=0)

# --- 🤖 Gemini 세수 판독 AI ---
def verify_wash_face(image_bytes):
    if "GEMINI_API_KEY" not in st.secrets:
        return False, "Streamlit Secrets에 GEMINI_API_KEY를 등록해주세요!"
    try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        prompt = """
        당신은 잠을 깨우는 엄격한 알람 요정입니다. 
        사진의 인물이 '세수를 마친 촉촉한 얼굴'이거나 '잠이 깨서 눈을 크게 뜬 얼굴'인지 판독하세요.
        반드시 다음 JSON 형식으로만 답하세요:
        {"success": true 또는 false, "comment": "위트있는 잔소리 1문장"}
        """
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=[types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"), prompt],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        import json
        result = json.loads(response.text)
        return result.get("success", False), result.get("comment", "판독 불가")
    except Exception as e:
        return False, f"AI 오류 발생: {str(e)}"

# --- 🎮 세션 상태 초기화 ---
if "state" not in st.session_state:
    st.session_state.state = "SETUP"  # SETUP -> WAITING -> RINGING -> CLEAR
if "target_time" not in st.session_state:
    st.session_state.target_time = None
if "math_num1" not in st.session_state:
    st.session_state.math_num1 = random.randint(11, 99)
    st.session_state.math_num2 = random.randint(11, 99)

# --- 📱 화면 구성 ---
st.title("🚨 잠 깨! 폭풍 기상 알람 미니게임")

# [1단계] 세팅 화면
if st.session_state.state == "SETUP":
    st.subheader("⏱️ 알람 시간 예약")
    alarm_time = st.time_input("알람이 울릴 시간 설정", datetime.now().time())
    test_mode = st.checkbox("🔥 즉시 테스트 모드 (5초 뒤 작동)")
    
    if st.button("⏰ 알람 가동 (이제 못 도망칩니다)", use_container_width=True):
        if test_mode:
            st.session_state.target_time = time.time() + 5
        else:
            now = datetime.now()
            target = datetime.combine(now.date(), alarm_time)
            if target < now:
                st.session_state.target_time = target.timestamp() + 86400
            else:
                st.session_state.target_time = target.timestamp()
        st.session_state.state = "WAITING"
        st.rerun()

# [2단계] 대기 화면
elif st.session_state.state == "WAITING":
    st.warning("🔒 알람이 세팅되었습니다. 지정된 시간에 폭풍 소리가 울립니다.")
    remains = int(st.session_state.target_time - time.time())
    
    if remains > 0:
        st.metric("알람 발동까지 남은 시간", f"{remains}초")
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.state = "RINGING"
        st.rerun()

# [3단계] 알람 발생 및 미니게임 미션
elif st.session_state.state == "RINGING":
    play_sound("alarm")  # 엄청난 사이렌 무한 반복 시작
    st.error("📢🚨🔥
