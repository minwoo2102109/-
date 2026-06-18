import streamlit as st
import time
from datetime import datetime
import json
import urllib.request
import base64

# 페이지 설정 (컴팩트하고 직관적인 레이아웃)
st.set_page_config(page_title="세수 인증 절대 알람", page_icon="🧼", layout="centered")

# --- 🔊 엄청난 알람 소리 및 효과음 재생 함수 ---
def play_sound(sound_type):
    """HTML5 오디오를 활용해 브라우저에서 강제로 효과음을 재생"""
    urls = {
        "alarm": "https://actions.google.com/sounds/v1/alarms/mechanical_clock_ring.ogg",
        "success": "https://actions.google.com/sounds/v1/cheering/applause_yeehaw.ogg",
        "fail": "https://actions.google.com/sounds/v1/cartoon/slide_whistle_down.ogg"
    }
    url = urls.get(sound_type)
    if url:
        # 알람음은 해제 전까지 무한 반복(loop) 설정
        loop = "loop" if sound_type == "alarm" else ""
        html = f'<audio autoplay {loop} style="display:none;"><source src="{url}" type="audio/ogg"></audio>'
        st.components.v1.html(html, height=0)

# --- 🤖 순수 HTTP 기반의 초경량 Gemini API 호출 ---
def verify_wash_face_api(image_bytes):
    if "GEMINI_API_KEY" not in st.secrets:
        return False, "Streamlit Secrets에 GEMINI_API_KEY를 등록해주세요."
    
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    
    # 이미지 base64 인코딩
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = """
    당신은 절대 타협하지 않는 엄격한 기상 감독관입니다.
    보내진 사진 속 인물이 '방금 세수를 마쳐서 얼굴에 물기가 있거나 촉촉한 상태'인지, 혹은 '잠이 완벽히 깨서 눈을 똑바로 뜨고 있는지' 엄격하게 판독하세요.
    대충 이불 속에서 찍었거나 여전히 졸린 눈이면 무조건 탈락입니다.
    
    응답은 시스템 연동을 위해 다른 설명 없이 오직 아래 JSON 양식으로만 답변하세요:
    {"success": true 또는 false, "comment": "잠을 깨우는 독설이나 위트있는 잔소리 한마디"}
    """
    
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
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            res_body = json.loads(response.read().decode('utf-8'))
            text_res = res_body['candidates'][0]['content']['parts'][0]['text']
            result = json.loads(text_res)
            return result.get("success", False), result.get("comment", "인증 완료")
    except Exception as e:
        return False, "얼굴을 인식하지 못했습니다. 눈을 크게 뜨고 밝은 곳에서 다시 찍으세요!"

# --- 앱 상태 관리 (간결화) ---
if "step" not in st.session_state:
    st.session_state.
