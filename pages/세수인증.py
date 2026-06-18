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
    
    prompt = "사진 속 인물이 세수를 완료했거나 잠이 깨서 눈을 똑바로 떴는지 판독하세요. 다른 설명 없이 오직 이 JSON 양식으로만 답변하세요: {\"success\": true 또는 false, \"comment\": \"잔소리 한마디\"}"
    
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
    is_test = st.checkbox("🔥 5초 뒤 즉시 울리기 (테스트)", value=True) # 기본 체크로 변경
    
    if st.button("알람 잠금 및 시작", use_container_width=True):
        if is_test:
            st.session_state["target"] = time.time() + 5
        else:
            now = datetime.now()
            tgt = datetime.combine(now.date(), t_input)
            st.session_state["target"] = tgt.timestamp() if tgt >= now else tgt.timestamp() + 86400
        st.session_state["step"] = "WAIT"
        st.rerun()

# [2 단계] 대기 화면 (실시간 타이머 개선)
elif st.session_state["step"] == "WAIT":
    st.warning("🔒 알람 시스템 작동 중")
    
    # 카운트다운을 위한 실시간 표시 영역 선언
    countdown_place = st.empty()
    
    while True:
        remains = int(st.session_state["target"] - time.time())
        if remains > 0:
            # 전체 화면 리런 대신 요소만 계속 업데이트하여 시간이 깎이는 것을 보여줌
            countdown_place.metric("알람까지 남은 시간", f"{remains}초")
            time.sleep(1)
        else:
            break
            
    # 시간이 다 되면 다음 단계로 진입 후 새로고침
    st.session_state["step"] = "RING"
    st.rerun()

# [3 단계] 알람 울림 및 카메라 촬영 화면
elif st.session_state["step"] == "RING":
    play_sound("alarm")
    st.error("🚨🚨🚨 폭풍 알람 발동!!! 당장 세수하고 오세요!!! 🚨🚨🚨")
    
    img = st.camera_input("방금 세수한 얼굴을 인증해 주세요!")
    
    if img is not None:
        image_bytes = img.getvalue()
        with st.spinner("Gemini가 눈빛과 물기를 분석 중..."):
            success, comment = verify_wash_face_api(image_bytes)
        
        st.session_state["comment"] = comment
        if success:
            st.session_state["step"] = "SUCCESS"
        else:
            st.session_state["step"] = "FAIL"
        st.rerun()

# [4 단계 - 성공] 알람 해제 완료 화면
elif st.session_state["step"] == "SUCCESS":
    play_sound("success")
    st.balloons()
    st.success("🎉 미션 성공! 완벽하게 기상하셨습니다!")
    st.info(f"💬 Gemini의 한마디: {st.session_state['comment']}")
    
    if st.button("처음으로 돌아가기", use_container_width=True):
        st.session_state["step"] = "SETUP"
        st.rerun()

# [4 단계 - 실패] 재인증 요구 화면
elif st.session_state["step"] == "FAIL":
    play_sound("fail")
    st.error("❌ 미션 실패! 아직 비몽사몽이거나 세수를 안 하셨군요?")
    st.warning(f"😈 Gemini의 팩트 폭행: {st.session_state['comment']}")
    
    if st.button("다시 인증 시도하기", use_container_width=True):
        st.session_state["step"] = "RING"
        st.rerun()
