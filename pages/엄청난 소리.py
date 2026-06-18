import streamlit as st
import time
import random
import datetime

# 페이지 설정
st.set_page_config(
    page_title="악마의 강제 기상 알람",
    page_icon="⏰",
    layout="centered"
)

# 세션 상태 초기화 (알람 상태 유지용)
if "alarm_triggered" not in st.session_state:
    st.session_state.alarm_triggered = False
if "math_problem" not in st.session_state:
    st.session_state.math_problem = None
if "math_answer" not in st.session_state:
    st.session_state.math_answer = None
if "selected_sound" not in st.session_state:
    st.session_state.selected_sound = None

# 상상치도 못한 엄청난 소리 리스트 (오디오 합성 링크 및 효과음)
SOUNDS = {
    "🚨 저세상 지구멸망 고주파 경보음": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", # 예시 고볼륨 음악
    "📢 8비트 레트로 엇박자 싸이렌": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "🐓 분노조절장애 수탉의 절규": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
}

# 랜덤 수학 문제 생성 함수
def generate_math_problem():
    num1 = random.randint(11, 99)
    num2 = random.randint(11, 99)
    operator = random.choice(["+", "-"])
    if operator == "+":
        ans = num1 + num2
    else:
        ans = num1 - num2
    return f"{num1} {operator} {num2} = ?", ans

# 앱 UI 시작
st.title("⏰ 악마의 강제 기상 알람기")
st.subheader(""상상치도 못한 소리"와 "정신 번쩍 문제"의 콜라보")
st.write("Streamlit Cloud에서 완벽하게 작동하는 아침 기상 보장 솔루션입니다.")

---

# 1. 알람 설정 섹션
st.header("1. 알람 예약 설정")
col1, col2 = st.columns(2)

with col1:
    target_time = st.time_input("언제 일어날 예정인가요?", datetime.time(7, 0))

with col2:
    sound_choice = st.selectbox("잠을 깨워줄 엄청난 소리 선택", list(SOUNDS.keys()))

# 현재 시간 표시
now = datetime.datetime.now().time()
st.info(f"현재 서버/브라우저 시간: {now.strftime('%H:%M:%S')}")

# 알람 시작 버튼
if st.button("⏰ 강제 기상 모드 가동", type="primary"):
    st.session_state.alarm_triggered = False
    st.success(f"[{target_time.strftime('%H:%M')}]에 지옥의 알람이 예약되었습니다. 이 창을 절대 닫지 마세요!")
    
    # 시간 체크 루프 (간단하고 안정적인 방식)
    placeholder = st.empty()
    while True:
        current_now = datetime.datetime.now().time()
        # 시/분이 일치하면 알람 트리거
        if current_now.hour == target_time.hour and current_now.minute == target_time.minute:
            st.session_state.alarm_triggered = True
            if st.session_state.math_problem is None:
                prob, ans = generate_math_problem()
                st.session_state.math_problem = prob
                st.session_state.math_answer = ans
                st.session_state.selected_sound = SOUNDS[sound_choice]
            break
        
        # 대기 상태 화면 표시
        placeholder.text(f"⏳ 알람 대기 중... 현재 시간: {current_now.strftime('%H:%M:%S')}")
        time.sleep(1)
    st.rerun()

---

# 2. 알람 발동 섹션 (알람이 켜졌을 때만 보임)
if st.session_state.alarm_triggered:
    st.error("🚨🚨🚨 기상!!! 기상!!! 상상치도 못한 소리가 울리는 중입니다!!! 🚨🚨🚨")
    
    # [핵심 기능] HTML5 Audio 오토플레이 활용 (Streamlit Cloud 우회 소리 재생)
    # 브라우저 보안 정책상 사용자가 페이지와 상호작용이 한 번 이상 있어야 소리가 납니다.
    audio_html = f"""
        <audio autoplay loop>
            <source src="{st.session_state.selected_sound}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
    """
    st.components.v1.html(audio_html, height=0)
    
    # 시각적 공포 효과
    st.warning("⚠️ 문제를 맞추기 전까지는 이 소리는 절대 멈추지 않습니다!")
    
    # 수학 문제 풀기 구역
    st.markdown(f"### 🧮 미션: 다음 문제를 해결하고 침대를 탈출하세요!")
    st.subheader(f"👉 {st.session_state.math_problem}")
    
    user_ans = st.number_input("정답 입력:", step=1, value=0)
    
    if st.button("🔓 알람 해제하기", type="secondary"):
        if user_ans == st.session_state.math_answer:
            st.balloons()
            st.success("🎉 정답입니다! 알람이 해제되었습니다. 좋은 하루 되세요!")
            # 상태 초기화
            st.session_state.alarm_triggered = False
            st.session_state.math_problem = None
            st.session_state.math_answer = None
            time.sleep(3)
            st.rerun()
        else:
            st.error("❌ 틀렸습니다! 소리가 더 크게 느껴지는 건 기분 탓이 아닙니다. 다시 푸세요!")
