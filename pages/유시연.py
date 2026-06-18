import streamlit as st
import datetime
import time
import random
import cv2
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Wake Quest",
    page_icon="⏰",
    layout="centered"
)

# -------------------------
# 상태 초기화
# -------------------------

if "alarm_set" not in st.session_state:
    st.session_state.alarm_set = False

if "alarm_triggered" not in st.session_state:
    st.session_state.alarm_triggered = False

if "face_verified" not in st.session_state:
    st.session_state.face_verified = False

if "game_passed" not in st.session_state:
    st.session_state.game_passed = False

if "target_time" not in st.session_state:
    st.session_state.target_time = None

if "game_number" not in st.session_state:
    st.session_state.game_number = random.randint(100, 999)

# -------------------------
# 효과음
# -------------------------

def play_alarm():
    st.markdown("""
    <audio autoplay loop>
      <source src="https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3" type="audio/mpeg">
    </audio>
    """, unsafe_allow_html=True)

def play_success():
    st.markdown("""
    <audio autoplay>
      <source src="https://www.soundjay.com/buttons/sounds/button-3.mp3" type="audio/mpeg">
    </audio>
    """, unsafe_allow_html=True)

# -------------------------
# 얼굴 인증
# -------------------------

def detect_face(image):
    try:
        img = np.array(image)

        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        return len(faces) > 0

    except Exception:
        return False

# -------------------------
# UI
# -------------------------

st.title("⏰ Wake Quest")
st.subheader("얼굴 인증 + 미니게임으로 알람 해제")

# -------------------------
# 알람 설정
# -------------------------

if not st.session_state.alarm_set:

    alarm_time = st.time_input(
        "알람 시간 설정",
        value=datetime.time(7, 0)
    )

    if st.button("알람 시작"):
        st.session_state.target_time = alarm_time
        st.session_state.alarm_set = True
        st.success("알람이 설정되었습니다.")
        st.rerun()

# -------------------------
# 알람 대기
# -------------------------

elif (
    st.session_state.alarm_set
    and not st.session_state.alarm_triggered
):

    now = datetime.datetime.now().time()

    st.info(
        f"설정 시간 : {st.session_state.target_time}"
    )

    st.write(
        f"현재 시간 : {now.strftime('%H:%M:%S')}"
    )

    if (
        now.hour == st.session_state.target_time.hour
        and now.minute == st.session_state.target_time.minute
    ):
        st.session_state.alarm_triggered = True
        st.rerun()

    st.caption("시간 확인을 위해 새로고침(F5) 해주세요.")

# -------------------------
# 알람 울림
# -------------------------

elif (
    st.session_state.alarm_triggered
    and not st.session_state.face_verified
):

    play_alarm()

    st.error("🚨 기상 미션 시작!")
    st.markdown("### 세수 후 얼굴을 촬영하세요")

    photo = st.camera_input(
        "얼굴 인증"
    )

    if photo is not None:

        try:
            image = Image.open(photo)

            if detect_face(image):

                st.session_state.face_verified = True
                play_success()

                st.success("얼굴 인증 성공!")
                st.rerun()

            else:
                st.warning(
                    "얼굴이 감지되지 않았습니다."
                )

        except Exception as e:
            st.error(
                f"이미지 처리 오류: {e}"
            )

# -------------------------
# 미니게임
# -------------------------

elif (
    st.session_state.face_verified
    and not st.session_state.game_passed
):

    st.success("얼굴 인증 완료")

    st.markdown("## 🎮 숫자 기억하기")

    st.info(
        f"이 숫자를 기억하세요: {st.session_state.game_number}"
    )

    st.write("5초 후 입력하세요.")

    time.sleep(5)

    st.markdown("---")

    answer = st.text_input(
        "숫자를 입력하세요"
    )

    if st.button("제출"):

        if answer == str(st.session_state.game_number):

            st.session_state.game_passed = True
            play_success()
            st.rerun()

        else:
            st.error("틀렸습니다!")

# -------------------------
# 성공
# -------------------------

elif st.session_state.game_passed:

    st.balloons()

    st.success(
        "🎉 기상 퀘스트 완료!"
    )

    st.markdown("""
    # ☀️ 좋은 아침입니다!
    알람이 해제되었습니다.
    """)

    if st.button("다시 시작"):

        st.session_state.alarm_set = False
        st.session_state.alarm_triggered = False
        st.session_state.face_verified = False
        st.session_state.game_passed = False
        st.session_state.game_number = random.randint(100, 999)

        st.rerun()
