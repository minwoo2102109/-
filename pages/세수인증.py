import streamlit as st
import time
from datetime import datetime
import random
import json
import urllib.request

# 페이지 설정
st.set_page_config(page_title="폭풍 알람", page_icon="🚨", layout="centered")

# --- 🔊 효과음 재생 함수 ---
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

# --- 🤖 라이브러리 충돌 우려 없는 순수 HTTP Gemini API 호출 ---
def verify_wash_face_api(image_bytes):
    if "GEMINI_API_KEY" not in st.secrets:
        return False, "API 키가 Secrets에 없습니다."
    
    api_key = st.secrets["GEMINI_API_KEY"]
    # 2026년 표준 gemini-2.5-flash-lite 엔드포인트 URL
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    
    import base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = "사진 속 인물이 세수를 완료했거나 잠이 깨서 눈을 똑바로 떴는지 판독하세요. 응답은 반드시 다른 말 없이 오직 이 JSON 양식으로만 하세요: {\"success\": true 또는 false, \"comment\": \"위트있는 잔소리 한마디\"}"
    
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
            return result.get("success", False), result.get("comment", "분석 완료")
    except Exception as e:
        return False, f"판독 실패 (세수하고 눈을 더 크게 뜨고 재시도해보세요!)"

# --- 세션 초기화 ---
if "step" not in st.session_state:
    st.session_state.step = "SETUP"
if "target" not in st.session_state:
    st.session_state.target = None
if "num1" not in st.session_state:
    st.session_state.num1 = random.randint(15, 99)
    st.session_state.num2 = random.randint(15, 99)

st.title("🚨 잠 깨! 폭풍 기상 알람 미니게임")

# [1단계] 설정
if st.session_state.step == "SETUP":
    st.subheader("⏱️ 알람 시간 설정")
    t_input = st.time_input("시간 선택", datetime.now().time())
    is_test = st.checkbox("🔥 5초 뒤 즉시 울리기 (테스트)")
    
    if st.button("알람 가동 시작", use_container_width=True):
        if is_test:
            st.session_state.target = time.time() + 5
        else:
            now = datetime.now()
            tgt = datetime.combine(now.date(), t_input)
            st.session_state.target = tgt.timestamp() if tgt >= now else tgt.timestamp() + 86400
        st.session_state.step = "WAIT"
        st.rerun()

# [2단계] 대기
elif st.session_state.step == "WAIT":
    st.warning("🔒 시스템 작동 중... 지정된 시간에 사이렌이 울립니다.")
    remains = int(st.session_state.target - time.time())
    if remains > 0:
        st.metric("알람까지 남은 시간", f"{remains}초")
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.step = "RING"
        st.rerun()

# [3단계] 알람 발동 및 미션
elif st.session_state.step == "RING":
    play_sound("alarm")
    st.error("📢🚨🔥 폭풍 알람 발동!!! 당장 일어나세요!!! 🔥🚨📢")
    
    st.subheader("🎮 [미션 1] 암산으로 정신 차리기")
    n1, n2 = st.session_state.num1, st.session_state.num2
    ans = st.number_input(f"{n1} + {n2} = ?", value=0, step=1)
    
    if ans == (n1 + n2):
        st.success("✅ 암산 성공! 마지막 2단계: 세수 인증 카메라 활성화")
        
        img = st.camera_input("카메라를 보고 세수한 촉촉한 얼굴을 인증하세요!")
        if img is not None:
            with st.spinner("AI 감독관 판독 중..."):
                success, comment = verify_wash_face_api(img.getvalue())
                if success:
                    play_sound("success")
                    st.session_state.step = "CLEAR"
                    st.rerun()
                else:
                    play_sound("fail")
                    st.error(f"❌ 실패: {comment}")
    else:
        st.info("정답을 맞혀야 아래에 세수 인증 카메라가 켜집니다.")

# [4단계] 클리어
elif st.session_state.step == "CLEAR":
    st.balloons()
    st.success("🎉 완벽합니다! 무사히 일어났습니다. 좋은 하루 되세요!")
    if st.button("🔄 처음으로 돌아가기", use_container_width=True):
        st.session_state.step = "SETUP"
        st.session_state.num1 = random.randint(15, 99)
        st.session_state.num2 = random.randint(15, 99)
        st.rerun()
