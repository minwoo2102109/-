import random
import time
import streamlit as st

# 1. 페이지 기본 설정 및 스타일
st.set_page_config(page_title="알람 브레이커 미니게임", page_icon="⏰", layout="centered")

st.markdown(
    """
    <style>
    .main-title { font-size: 2.5rem; font-weight: bold; text-align: center; color: #FF4B4B; margin-bottom: 10px; }
    .status-box { padding: 15px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px; text-align: center; }
    .game-box { padding: 25px; border-radius: 15px; border: 2px solid #FF4B4B; background-color: #ffffff; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
    .pass-text { color: #28a745; font-size: 1.5rem; font-weight: bold; }
    .alarm-on-text { color: #dc3545; font-size: 1.2rem; font-weight: bold; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. 게임 상태(State) 및 알람 설정 초기화
TARGET_SCORE = 60  # 통과 조건 점수

# 저작권 프리 알람 사운드 URL (웹에서 바로 스트리밍 가능하고 안정적인 주소)
ALARM_URL = "https://google.com"

if "score" not in st.session_state:
    st.session_state.score = 0
if "current_game" not in st.session_state:
    st.session_state.current_game = None
if "game_stage" not in st.session_state:
    st.session_state.game_stage = "START"  # START, PLAYING, FINISHED
if "game_data" not in st.session_state:
    st.session_state.game_data = {}


# 3. 게임 로직 제어 함수
def start_new_game():
    """무작위로 새로운 미니게임을 선정하고 데이터를 세팅합니다."""
    games = ["click_speed", "math_genius", "color_match"]
    st.session_state.current_game = random.choice(games)

    if st.session_state.current_game == "click_speed":
        st.session_state.game_data = {"pos": random.choice(["좌측", "중앙", "우측"])}

    elif st.session_state.current_game == "math_genius":
        num1 = random.randint(10, 50)
        num2 = random.randint(1, 9)
        op = random.choice(["+", "-", "*"])
        ans = eval(f"{num1}{op}{num2}")
        st.session_state.game_data = {"q": f"{num1} {op} {num2} = ?", "ans": ans}

    elif st.session_state.current_game == "color_match":
        colors = {"빨강": "red", "파랑": "blue", "초록": "green", "노랑": "orange"}
        word = random.choice(list(colors.keys()))
        display_color_name = random.choice(list(colors.keys()))
        color_code = colors[display_color_name]
        is_match = "일치" if word == display_color_name else "불일치"
        st.session_state.game_data = {
            "word": word,
            "color_code": color_code,
            "ans": is_match,
        }


def reset_all():
    """전체 게임 상태를 초기화합니다."""
    st.session_state.score = 0
    st.session_state.game_stage = "PLAYING"
    start_new_game()


# 4. 오디오 재생 시스템 (알람 제어)
def play_alarm(url):
    """HTML5 오디오 태그를 숨겨서 무한 반복(loop) 재생합니다."""
    html_string = f"""
    <audio autoplay loop>
        <source src="{url}" type="audio/ogg">
    </audio>
    """
    st.markdown(html_string, unsafe_allow_html=True)


# 5. 화면 레이아웃 구성
st.markdown(
    "<div class='main-title'>⏰ 알람 브레이커 챌린지</div>", unsafe_allow_html=True
)
st.write(
    f"점수를 획득해 알람을 끄세요! **목표 점수: {TARGET_SCORE}점**을 넘어야 소리가 꺼집니다."
)

# 대시보드 (현재 점수 및 알람 상태 표시)
alarm_status_html = ""
if st.session_state.game_stage == "PLAYING":
    alarm_status_html = (
        "<p class='alarm-on-text'>🚨 알람 작동 중! 미니게임을 푸세요! 🚨</p>"
    )
elif st.session_state.game_stage == "FINISHED":
    alarm_status_html = "<p style='color:#28a745; font-weight:bold;'>✅ 알람 해제 완료</p>"

st.markdown(
    f"""
    <div class='status-box'>
        <h3>현재 점수: <span style='color:#FF4B4B;'>{st.session_state.score}</span> / {TARGET_SCORE} 점</h3>
        {alarm_status_html}
    </div>
    """,
    unsafe_allow_html=True,
)


# 6. 게임 스테이지별 화면 및 알람 제어
# [STAGE 1] 시작 화면
if st.session_state.game_stage == "START":
    st.warning(
        "⚠️ 주의: 시작 버튼을 누르면 알람 소리가 무한 반복됩니다! 볼륨을 조절하세요."
    )
    if st.button("🔔 알람 시작 및 게임 풀기", use_container_width=True):
        reset_all()
        st.rerun()

# [STAGE 2] 게임 진행 화면 (알람 울리는 중)
elif st.session_state.game_stage == "PLAYING":
    # 💥 중요: 게임 중에는 알람 음원을 계속 재생함 (통과하기 전까지 무한 반복)
    play_alarm(ALARM_URL)

    st.markdown("<div class='game-box'>", unsafe_allow_html=True)

    try:
        # --- 미니게임 A: 순발력 클릭 ---
        if st.session_state.current_game == "click_speed":
            st.subheader("🎯 미니게임: 순발력 클릭!")
            target_pos = st.session_state.game_data.get("pos", "중앙")
            st.write(f"지금 누를 위치: **[{target_pos}]**")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🎯 여기!", key="btn_l", use_container_width=True):
                    if target_pos == "좌측":
                        st.session_state.score += 15
                    else:
                        st.session_state.score -= 10
                    start_new_game()
                    st.rerun()
            with col2:
                if st.button("🎯 여기!", key="btn_m", use_container_width=True):
                    if target_pos == "중앙":
                        st.session_state.score += 15
                    else:
                        st.session_state.score -= 10
                    start_new_game()
                    st.rerun()
            with col3:
                if st.button("🎯 여기!", key="btn_r", use_container_width=True):
                    if target_pos == "우측":
                        st.session_state.score += 15
                    else:
                        st.session_state.score -= 10
                    start_new_game()
                    st.rerun()

        # --- 미니게임 B: 암산 천재 ---
        elif st.session_state.current_game == "math_genius":
            st.subheader("🧮 미니게임: 암산 천재!")
            question = st.session_state.game_data.get("q", "0 + 0 = ?")
            correct_ans = st.session_state.game_data.get("ans", 0)

            st.markdown(f"### `{question}`")

            options = list(
                set([correct_ans, correct_ans + 5, correct_ans - 3, correct_ans * 2])
            )
            random.shuffle(options)

            cols = st.columns(len(options))
            for i, opt in enumerate(options):
                with cols[i]:
                    if st.button(str(opt), key=f"math_{i}", use_container_width=True):
                        if opt == correct_ans:
                            st.session_state.score += 20
                        else:
                            st.session_state.score -= 5
                        start_new_game()
                        st.rerun()

        # --- 미니게임 C: 색상 일치 퀴즈 ---
        elif st.session_state.current_game == "color_match":
            st.subheader("🎨 미니게임: 색상 불일치 극복!")
            word = st.session_state.game_data.get("word", "빨강")
            color_code = st.session_state.game_data.get("color_code", "red")
            correct_ans = st.session_state.game_data.get("ans", "일치")

            st.markdown(
                f"### <span style='color:{color_code}; font-size:3rem;'>{word}</span>",
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("⭕ 일치", use_container_width=True):
                    if correct_ans == "일치":
                        st.session_state.score += 15
                    else:
                        st.session_state.score -= 10
                    start_new_game()
                    st.rerun()
            with col2:
                if st.button("❌ 불일치", use_container_width=True):
                    if correct_ans == "불일치":
                        st.session_state.score += 15
                    else:
                        st.session_state.score -= 10
                    start_new_game()
                    st.rerun()

    except Exception as e:
        start_new_game()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 실시간 점수 조건 체크 (목표 달성 시 오디오 재생을 누락시켜 알람을 끔)
    if st.session_state.score >= TARGET_SCORE:
        st.session_state.game_stage = "FINISHED"
        st.rerun()


# [STAGE 3] 결과 화면 (성공하여 알람이 꺼진 상태)
elif st.session_state.game_stage == "FINISHED":
    st.markdown("<div class='game-box'>", unsafe_allow_html=True)

    st.markdown(
        "<p class='pass-text'>🎉 알람 해제 성공! 🎉</p>", unsafe_allow_html=True
    )
    st.balloons()
    st.write(
        f"미션을 완료하여 시끄러운 알람을 껐습니다! (최종 점수: {st.session_state.score}점)"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔄 다시 알람 켜기", use_container_width=True):
        reset_all()
        st.rerun()

