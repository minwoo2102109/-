import streamlit as st
import time
from datetime import datetime
import json
import urllib.request
import base64

# 1. 페이지 기본 설정
st.set_page_config(page_title="세수 알람", page_icon="🧼", layout="centered")

# 2. 알람 및 효과음 재생 함수
def play_sound(sound_type):
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

# 3. Gemini API 활용 세수 및 잠 깨어남 판독 함수
def verify_wash_face_api(image_bytes):
    if "GEMINI_API_KEY" not in st.secrets:
        return False, "API 키가 없습니다."
    
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = "사진 속 인물이 세수를 완료했거나 잠이 깨서 눈을 똑바로 떴인지 판독하세요. 다른 설명 없이 오직 이 JSON 양식으로만 답변하세요: {\"success\": true 또는 false, \"comment\": \"잔소리 한마디\"}"
    
    data = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inlineData": {"mimeType": "image/jpeg", "data": base64_image}}
            ]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=15) as response:
            res_body = json.loads(response.read().decode('utf-8'))
            text_res = res_body['candidates'][0]['content']['parts'][0]['text']
            result = json.loads(text_res)
            return result.get("success", False), result.get("comment", "완료")
    except Exception:
        return False, "다시 촬영해 주세요."

# 4. 세션 상태(Session State) 초기화
if "step" not in st.session_state:
    st.session_state["step"] = "SETUP"
if "target" not in st.session_state:
    st.session_state["target"] = None
if "comment" not in st.session_state:
    st.session_state["comment"] = ""

st.title("🚨 세수 인증 기상 시스템")

# --- 단계별 화면 구현 ---

# [1 단계] 알람 예약 화면
if st.session_state["step"] == "SETUP":
    st.subheader("⏱️ 알람 시간 설정")
    t_input = st.time_input("시간 선택", datetime.now().time())
    is_test = st.checkbox("🔥 5초 뒤 즉시 울리기 (테스트)")
    
    if st.button("알람 잠금 및 시작", use_container_width=True):
        if is_test:
            st.session_state["target"] = time.time() + 5
        else:
            now = datetime.now()
            tgt = datetime.combine(now.date(), t_input)
            st.session_state["target"] = tgt.timestamp()
