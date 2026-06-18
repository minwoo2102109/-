import random
import time
import streamlit as st

# 1. 페이지 기본 설정 및 스타일
st.set_page_config(page_title="랜덤 미니게임 챌린지", page_icon="🎮", layout="centered")

# 커스텀 CSS로 UI 차별화 (깔끔한 게임 아케이드 느낌)
st.markdown(
    """
    <style>
    .main-title { font-size: 2.5rem; font-weight: bold; text-align: center; color: #FF4B4B; margin-bottom: 10px; }
    .status-box { padding: 15px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px; text-align: center; }
    .game-box { padding: 25px; border-radius: 15px; border: 2px solid #FF4B4B; background-color: #ffffff; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); }
    .pass-text { color: #28a745; font-size: 1.5rem; font-weight: bold; }
    .fail-text { color: #dc3545; font-size: 1.5rem; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. 게임 상태(State) 초기화
TARGET_SCORE = 60  # 통과 조건 점수

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
    # 직전 게임과 겹치지 않게 선택 (옵션)
    st.session_state.current_game = random.choice(games)

    # 게임별 초기 데이터 생성
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
        # 글자 의미와 실제 색상이 일치하는지 여부
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


# 4. 화면 레이아웃 구성
st.markdown(
    "<div class='main-title'>🎲 랜덤 미니게임 챌린지</div>", unsafe_allow_html=True
)
st.write(
    f"무작위로 나오는 게임을 해결하세요! **목표 점수: {TARGET_SCORE}점**을 넘어야 통과합니다."
)

# 대시보드 (현재 점수 표시)
st.markdown(
    f"""
    <div class='status-box'>
        <h3>현재 점수: <span style='color:#FF4B4B;'>{st.session_state.score}</span> / {TARGET_SCORE} 점</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# 5. 게임 스테이지별 화면 렌더링
# [STAGE 1] 시작 화면
if st.session_state.game_stage == "START":
    st.info("준비가 되셨다면 아래 버튼을 눌러 챌린지를 시작하세요!")
    if st.button("🚀 챌린지 시작", use_container_width=True):
        reset_all()
        st.rerun()

# [STAGE 2] 게임 진행 화면
elif st.session_state.game_stage == "PLAYING":
    st.markdown("<div class='game-box'>", unsafe_allow_html=True)

    try:
        # --- 미니게임 A: 순발력 클릭 ---
        if st.session_state.current_game == "click_speed":
            st.subheader("🎯 미니게임: 순발력 클릭!")
            st.caption("목표: 지정된 위치에 나타난 버튼을 빠르게 클릭하세요!")

            target_pos = st.session_state.game_data.get("pos", "중앙")
            st.write(
                f"지금 누를 위치: **[{target_pos}]**", font_size="1.2rem"
            )

            # 3열 레이아웃으로 버튼 분산 배치
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🎯 여기!", key="btn_l", use_container_width=True):
                    if target_pos == "좌측":
                        st.session_state.score += 15
                        st.success("+15점 획득!")
                    else:
                        st.session_state.score -= 10
                        st.error("오클릭! -10점")
                    start_new_game()
                    st.rerun()
            with col2:
                if st.button("🎯 여기!", key="btn_m", use_container_width=True):
                    if target_pos == "중앙":
                        st.session_state.score += 15
                        st.success("+15점 획득!")
                    else:
                        st.session_state.score -= 10
                        st.error("오클릭! -10점")
                    start_new_game()
                    st.rerun()
            with col3:
                if st.button("🎯 여기!", key="btn_r", use_container_width=True):
                    if target_pos == "우측":
                        st.session_state.score += 15
                        st.success("+15점 획득!")
                    else:
                        st.session_state.score -= 10
                        st.error("오클릭! -10점")
                    start_new_game()
                    st.rerun()

        # --- 미니게임 B: 암산 천재 ---
        elif st.session_state.current_game == "math_genius":
            st.subheader("🧮 미니게임: 암산 천재!")
            st.caption("목표: 수식을 계산하여 올바른 정답을 선택하세요!")

            question = st.session_state.game_data.get("q", "0 + 0 = ?")
            correct_ans = st.session_state.game_data.get("ans", 0)

            st.markdown(f"### `{question}`")

            # 오답 보기 생성
            options = list(
                set([correct_ans, correct_ans + 5, correct_ans - 3, correct_ans * 2])
            )
            random.shuffle(options)

            # 보기 버튼 생성
            cols = st.columns(len(options))
            for i, opt in enumerate(options):
                with cols[i]:
                    if st.button(str(opt), key=f"math_{i}", use_container_width=True):
                        if opt == correct_ans:
                            st.session_state.score += 20
                            st.success("정답입니다! +20점")
                        else:
                            st.session_state.score -= 5
                            st.error("틀렸습니다! -5점")
                        start_new_game()
                        st.rerun()

        # --- 미니게임 C: 색상 일치 퀴즈 ---
        elif st.session_state.current_game == "color_match":
            st.subheader("🎨 미니게임: 색상 불일치 극복!")
            st.caption("목표: 글자의 '의미'와 글자의 '실제 색상'이 일치하는지 맞추세요!")

            word = st.session_state.game_data.get("word", "빨강")
            color_code = st.session_state.game_data.get("color_code", "red")
            correct_ans = st.session_state.game_data.get("ans", "일치")

            # HTML을 사용하여 글자에 색상 입히기
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
        # 예기치 못한 게임 데이터 오류 시 세션 초기화 후 재시작
        start_new_game()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 패스 조건 감시 및 포기 버튼
    st.write("---")
    if st.session_state.score >= TARGET_SCORE:
        st.session_state.game_stage = "FINISHED"
        st.rerun()

    if st.button("🏳️ 챌린지 종료 (결과 보기)", use_container_width=True):
        st.session_state.game_stage = "FINISHED"
        st.rerun()


# [STAGE 3] 결과 화면
elif st.session_state.game_stage == "FINISHED":
    st.markdown("<div class='game-box'>", unsafe_allow_html=True)

    if st.session_state.score >= TARGET_SCORE:
        st.markdown(
            "<p class='pass-text'>🎉 챌린지 성공! 🎉</p>", unsafe_allow_html=True
        )
        st.balloons()
        st.write(
            f"최종 점수 **{st.session_state.score}점**으로 기준 점수({TARGET_SCORE}점)를 넘겼습니다!"
        )
    else:
        st.markdown(
            "<p class='fail-text'>😢 챌린지 실패 😢</p>", unsafe_allow_html=True
        )
        st.write(
            f"최종 점수는 **{st.session_state.score}점**입니다. 통과 기준({TARGET_SCORE}점)에 도달하지 못했습니다."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔄 다시 도전하기", use_container_width=True):
        reset_all()
        st.rerun()

