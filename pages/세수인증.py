import streamlit as st
import time
from datetime import datetime
import json
import urllib.request
import base64

# 페이지 설정
st.set_page_config(page_title="세수 인증 기상 알람", page_icon="🧼", layout="centered")

# --- 🔊 엄청난 알람 소리 및 효과음 재생 ---
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

# --- 🤖 순수 HTTP 내장 라이브러리 기반 Gemini API 호출 ---
def verify_wash_face_api(image_bytes):
    if "GEMINI_API_KEY" not in st.secrets:
        return False, "Streamlit Secrets에 GEMINI_API_KEY를 등록해주세요."
    
    api_key = st.secrets["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = """
    당신은 엄격한 기상 감독관입니다. 
    사진 속 인물이 방금 세수를 해서 얼굴에 물기가 남아있거나, 눈을 번쩍 뜨고 잠이 확실히 깼는지 판독하세요.
    응답은 반드시 다른 설명 없이 오직 아래 JSON 양식으로만 답변하세요:
    {"success": true 또는 false, "comment": "위트있고 까칠한 잔소리 한마디"}
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
            return result.get("success", False), result.get("comment", "인증 처리 완료")
    except Exception as e:
        return False, "눈을 더 크게 뜨고 정면을 다시 촬영해 주세요!"

# --- 앱 상태 관리 ---
if "step" not in st.session_state:
    st.session_state.step = "SETUP"
if "target" not in st.session_state:
    st.session_state.target = None

st.title("🧼 세수 인증 절대 알람")

# [1단계] 설정 화면
if st.session_state.step == "SETUP":
    st.subheader("⏱️ 알람 예약")
    t_input = st.time_input("알람 울릴 시간", datetime.now().time())
    is_test = st.checkbox("🔥 5초 뒤 즉시 알람 가동 (테스트용)")
    
    if st.button("알람 잠금 및 시작", use_container_width=True):
        if is_test:
            st.session_state.target = time.time() + 5
        else:
            now = datetime.now()
            tgt = datetime.combine(now.date(), t_input)
            st.session_state.target = tgt.timestamp() if tgt >= now else tgt.timestamp() + 86400
        st.session_state.step = "WAIT"
        st.rerun()

# [2단계] 시간 대기
elif st.session_state.step == "WAIT":
    st.warning("🔒 알람 시스템이 작동 중입니다. 다른 화면으로 벗어나지 마세요.")
    remains = int(st.session_state.target - time.time())
    if remains > 0:
        st.metric("알람 발동까지", f"{remains}초 전")
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.step = "RING"
        st.rerun()

# [3단계] 알람 해제 (오직 세수 인증만 존재)
elif st.session_state.step == "RING":
    play_sound("alarm")
    st.error("🚨🚨🚨 폭풍 알람 재생 중! 당장 세수하고 카메라를 보세요! 🚨🚨🚨")
    
    st.subheader("📸 세수 인증 미션")
    img = st.camera_input("방금 세수한 촉촉한 얼굴 촬영")
    
    if img is not None:
        with st.spinner("AI 감독관이 수분 상태 및 눈눈곱 확인 중..."):
            success, comment = verify_wash_face_api(img.getvalue())
            if success:
                play_sound("success")
                st.session_state.step = "CLEAR"
                st.rerun()
            else:
                play_sound("fail")
                st.error(f"❌ 인증 실패: {comment}")
                st.info("알람 소리가 바뀝니다! 다시 씻고 정확하게 찍으세요.")

# [4단계] 기상 해제 완료
elif st.session_state.step == "CLEAR":
    st.balloons()
    st.success("🎉 미션 성공! 소리가 완전히 꺼졌습니다. 상쾌한 하루 되세요!")
    if st.button("🔄 새 알람 맞추기", use_container_width=True):
        st.session_state.step = "SETUP"
        st.rerun()
