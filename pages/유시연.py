import streamlit as st
import time
from datetime import datetime
import base64
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 페이지 기본 설정
st.set_page_config(page_title="모닝 미션! 잠깨기 대작전", page_icon="⏰", layout="centered")

# --- 효과음 재생 함수 (HTML5 Audio 활용) ---
def play_sound(sound_type):
    """Streamlit에서 오디오를 자동 재생하기 위한 HTML 베이스64 오디오 태그 삽입"""
    sound_urls = {
        "alarm": "https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg",
        "success": "https://actions.google.com/sounds/v1/cartoon/slide_whistle_up.ogg",
        "fail": "https://actions.google.com/sounds/v1/cartoon/boing.ogg"
    }
    url = sound_urls.get(sound_type)
    if url:
        loop_attr = "loop" if sound_type == "alarm" else ""
        audio_html = f"""
            <audio autoplay {loop_attr} style="display:none;">
                <source src="{url}" type="audio/ogg">
            </audio>
        """
        st.components.v1.html(audio_html, height=0)

# --- Gemini AI 세수 인증 함수 ---
def verify_wash_face(image_bytes):
    """Gemini 2.5 Flash Lite를 사용하여 세수 여부 판독"""
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("🔒 Secrets에 GEMINI_API_KEY가 설정되지 않았습니다.")
        return False, "API 키 누락"
    
    try:
        # 2026년 최신 google-genai SDK 스타일 적용
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
        
        prompt = """
        당신은 잠을 깨우는 엄격한 알람 요정입니다. 
        제공된 사진의 인물이 '세수를 방금 마친 얼굴'이거나 '잠이 완전히 깨서 눈을 똑바로 뜬 얼굴'인지 판독해주세요.
        
        응답은 반드시 아래의 JSON 형식으로만 하세요. 다른 말은 절대 하지 마세요:
        {
          "success": true 또는 false (세수했거나 잠이 깼으면 true, 여전히 졸려보이거나 빈 사진이거나 대충 찍었으면 false),
          "comment": "사용자에게 한마디 (위트 있고 장난스러운 잔소리 톤, 2문장 이내)"
        }
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        # 결과 파싱
        import json
        result = json.loads(response.text)
        return result.get("success", False), result.get("comment", "분석 실패")
        
    except APIError as e:
        return False, f"AI 연결 오류가 발생했습니다: {str(e)}"
    except Exception as e:
        return False, f"오류 발생: {str(e)}"

# --- 앱 상태 관리 (Session State) ---
if "alarm_state" not in st.session_state:
    st.session_state.alarm_state = "ready"  # ready, waiting, ringing, clear
if "target_time" not in st.session_state:
    st.session_state.target_time = None

# --- UI 레이아웃 ---
st.title("⏰ 모닝 미션! 잠깨기 대작전")
st.caption("세수하고 촉촉한 얼굴을 인증하기 전까진 절대 꺼지지 않는 알람!")

# 1단계: 알람 설정 (Ready)
if st.session_state.alarm_state == "ready":
    st.subheader("🎯 1단계: 알람 설정하기")
    
    col1, col2 = st.columns(2)
    with col1:
        alarm_time = st.time_input("알람 울릴 시간 선택", datetime.now().time())
    with col2:
        test_mode = st.checkbox("🔥 5초 뒤 바로 울리기 (테스트용)")

    if st.button("🚀 알람 기상 모드 가동!", use_container_width=True):
        if test_mode:
            st.session_state.target_time = time.time() + 5
        else:
            now = datetime.now()
            target = datetime.combine(now.date(), alarm_time)
            if target < now:
                st.warning("이미 지나간 시간입니다! 내일 시간으로 설정됩니다.")
                st.session_state.target_time = target.timestamp() + 86400
            else:
                st.session_state.target_time = target.timestamp()
                
        st.session_state.alarm_state = "waiting"
        st.rerun()

# 2단계: 알람 대기중 (Waiting)
elif st.session_state.alarm_state == "waiting":
    st.info("⏳ 시스템 가동 중... 지정된 시간이 되면 미션이 시작됩니다.")
    
    # 남은 시간 표시
    remaining = int(st.session_state.target_time - time.time())
    if remaining > 0:
        st.metric(label="미션 발생까지 남은 시간", value=f"{remaining}초")
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.alarm_state = "ringing"
        st.rerun()

# 3단계: 알람 울림 & 미션 수행 (Ringing)
elif st.session_state.alarm_state == "ringing":
    st.error("🚨🚨🚨 삐비빅! 기상! 기상! 당장 세수하고 오세요! 🚨🚨🚨")
    play_sound("alarm") # 알람 소리 무한 루프 시작
    
    st.subheader("🧼 미션: 세수한 얼굴 인증하기")
    st.write("카메라를 켜고 방금 세수해서 물기가 남아있거나 눈을 번쩍 뜬 얼굴을 찍으세요!")
    
    # 웹캠 입력 받기
    img_file = st.camera_input("찰칵! 잠 깨기 인증샷")
    
    if img_file is not None:
        with st.spinner("AI 감독관이 눈곱과 물기를 확인하는 중..."):
            bytes_data = img_file.getvalue()
            success, comment = verify_wash_face(bytes_data)
            
            st.markdown(f"#### 🤖 AI 감독관의 평가:")
            if success:
                st.success(f"🟢 성공!! {comment}")
                play_sound("success")
                st.session_state.alarm_state = "clear"
                time.sleep(2) # 효과음 들을 시간 확보
                st.rerun()
            else:
                st.error(f"🔴 실패!! {comment}")
                play_sound("fail")
                st.info("다시 세수하고 오거나 눈을 크게 뜨고 다시 찍으세요!")

# 4단계: 알람 해제 완료 (Clear)
elif st.session_state.alarm_state == "clear":
    st.balloons()
    st.success("🎉 완벽합니다! 성공적으로 기상하셨습니다. 활기찬 하루 되세요!")
    
    if st.button("🔄 처음으로 돌아가기", use_container_width=True):
        st.session_state.alarm_state = "ready"
        st.session_state.target_time = None
        st.rerun()
