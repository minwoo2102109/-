
import streamlit as st
from google import genai
from google.genai import types
from google.genai.errors import APIError

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="알람 앱 기획 챗봇", page_icon="⏰")
st.title("⏰ Gemini 알람 앱 챗봇")
st.caption("Gemini 2.5 Flash Lite 모델을 사용한 AI 아이디어 파트너입니다.")

# 2. Streamlit Secrets에서 API 키 불러오기 및 클라이언트 초기화
try:
    # secrets.toml에 저장된 API 키 가져오기
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("Secrets에 'GEMINI_API_KEY'가 설정되지 않았습니다. .streamlit/secrets.toml 파일을 확인해주세요.")
    st.stop()
except Exception as e:
    st.error(f"초기화 중 오류가 발생했습니다: {e}")
    st.stop()

# 3. 세션 상태(Session State)를 활용한 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # 챗봇의 역할(페르소나)을 부여하는 시스템 지시어 설정
    system_instruction = (
        "당신은 혁신적이고 실용적인 모바일 알람 애플리케이션을 기획하는 전문 기획자입니다. "
        "사용자가 알람 앱 또는 다른 주제에 대해 질문하면, 창의적인 기능, UI/UX 개선안, "
        "차별화 전략 등을 친절하고 상세하게 제안해주세요."
    )
    
    # google-genai SDK의 새로운 방식으로 채팅 세션 시작
    try:
        st.session_state.chat = client.chats.create(
            model="gemini-2.5-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )
    except Exception as e:
        st.error(f"채팅 세션을 생성하는 중 오류가 발생했습니다: {e}")
        st.stop()

# 4. 이전 채팅 기록 화면에 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. 사용자 입력 처리
if user_input := st.chat_input("알람 앱에 대해 궁금한 점이나 아이디어를 입력하세요!"):
    
    # 사용자가 입력한 메시지 화면에 표시 및 세션 저장
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 6. Gemini API 호출 및 오류 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("💡 생각 중...")
        
        try:
            # 채팅 세션을 통해 답변 스트리밍 또는 단발성 메시지 전송
            # (여기서는 단순 send_message를 사용하되 예외 처리를 강화했습니다)
            response = st.session_state.chat.send_message(user_input)
            ai_response = response.text
            
            # 화면에 답변 업데이트 및 세션 저장
            message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except APIError as ae:
            # Gemini API 관련 에러 처리 (인증 실패, 할당량 초과 등)
            error_msg = f"⚠️ Gemini API 오류가 발생했습니다: {ae.message} (코드: {ae.code})"
            message_placeholder.markdown(error_msg)
        except Exception as e:
            # 기타 일반적인 에러 처리
            error_msg = f"⚠️ 예상치 못한 오류가 발생했습니다: {str(e)}"
            message_placeholder.markdown(error_msg)
