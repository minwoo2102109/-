import streamlit as st
import os
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 레이아웃 및 제목 설정
st.set_page_config(page_title="알람 브레이커 AI", page_icon="⏰")
st.title("⏰ 미니게임 알람 해제 챗봇")
st.caption("알람을 끄려면 AI가 출제하는 무작위 미니게임에서 목표 점수를 넘으세요!")

# 2. API 키 로드 및 클라이언트 초기화 (오류 처리 포함)
# 구글 AI 스튜디오 및 일반적인 secrets 도구(Streamlit, Replit 등)는 주로 환경 변수로 매핑됩니다.
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ 'GEMINI_API_KEY' 가 Secrets 혹은 환경 변수에 설정되지 않았습니다.")
    st.stop()

@st.cache_resource
def get_genai_client():
    try:
        # 최신 google-genai 클라이언트 생성
        return genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"클라이언트 초기화 중 오류 발생: {e}")
        return None

client = get_genai_client()

# 3. Streamlit 세션 상태(Chat History) 초기화 및 유지
if "messages" not in st.session_state:
    st.session_state.messages = []

# AI와의 대화 연속성을 유지하기 위해 채팅 세션 객체 보관
if "chat_session" not in st.session_state and client:
    system_instruction = (
        "너는 사용자의 잠을 깨우기 위해 알람 해제 미니게임을 진행하는 친절하고 유쾌한 AI 동반자야. "
        "사용자가 말을 걸면 즉시 무작위 미니게임(예: 3초 상식 퀴즈, 무작위 연산, 단어 거꾸로 말하기, 끝말잇기 등)을 시작해줘. "
        "게임마다 '통과 기준 점수'를 명확히 제시하고, 사용자의 답변을 평가하여 점수를 누적해줘. "
        "사용자가 목표 점수를 넘기면 [알람 해제 성공]이라는 키워드를 메시지에 반드시 포함해서 축하해줘야 해."
    )
    
    try:
        # 대화 기록(history) 유지를 위한 단일 chat 세션 인스턴스 생성
        st.session_state.chat_session = client.chats.create(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7
            )
        )
    except APIError as e:
        st.error(f"Gemini API 연결 실패: {e.message}")
        st.stop()
    except Exception as e:
        st.error(f"세션 초기화 실패: {e}")
        st.stop()

# 4. 화면에 기존 채팅 기록 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. 사용자 입력 처리 및 API 호출
if user_input := st.chat_input("답변을 입력하세요..."):
    # 사용자 입력 UI 렌더링 및 기록 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성 (에러 핸들링 포함)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        try:
            # 채팅 세션을 통해 기록을 유지하며 메시지 전송
            response = st.session_state.chat_session.send_message(user_input)
            ai_response = response.text
            
            # 응답 출력 및 기록 추가
            response_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
            # 미니게임 성공 여부 체크 시 시각적 효과 제공
            if "[알람 해제 성공]" in ai_response:
                st.balloons()
                st.success("🎉 축하합니다! 알람이 꺼졌습니다. 좋은 하루 되세요!")
                
        except APIError as api_err:
            error_msg = f"⚠️ Gemini API 오류가 발생했습니다: {api_err.message}"
            response_placeholder.markdown(error_msg)
        except Exception as e:
            error_msg = f"⚠️ 처리 중 예기치 못한 에러가 발생했습니다: {str(e)}"
            response_placeholder.markdown(error_msg)
