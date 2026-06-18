import streamlit as st
from datetime import datetime
import time
import cv2
import numpy as np

st.set_page_config(
    page_title="Wake & Wash",
    page_icon="⏰",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#87CEFA,#ffffff);
}

.title {
    text-align:center;
    font-size:50px;
    font-weight:bold;
    color:#0F4C81;
}

.subtitle{
    text-align:center;
    font-size:22px;
    color:#444;
}

.alarm-box{
    background:#ff4b4b;
    padding:20px;
    border-radius:20px;
    text-align:center;
    color:white;
    font-size:30px;
    font-weight:bold;
    animation: blink 1s infinite;
}

.success-box{
    background:#00c853;
    padding:20px;
    border-radius:20px;
    text-align:center;
    color:white;
    font-size:30px;
    font-weight:bold;
}

@keyframes blink{
    50%{
        opacity:0.4;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State
# -----------------------------
if "alarm_active" not in st.session_state:
    st.session_state.alarm_active = False

if "alarm_triggered" not in st.session_state:
    st.session_state.alarm_triggered = False

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="title">⏰ Wake & Wash 🚿</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">세수한 얼굴 인증 후에만 알람 종료 가능</div>',
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Current Time
# -----------------------------
now = datetime.now()

st.metric(
    "현재 시각",
    now.strftime("%H:%M:%S")
)

# -----------------------------
# Alarm Setting
# -----------------------------
alarm_time = st.time_input(
    "알람 시간 설정",
    value=datetime.now().time()
)

if st.button("알람 시작"):
    st.session_state.alarm_active = True
    st.success("알람이 활성화되었습니다.")

# -----------------------------
# Alarm Check
# -----------------------------
if st.session_state.alarm_active:

    current_time = datetime.now().strftime("%H:%M")
    target_time = alarm_time.strftime("%H:%M")

    st.info(f"설정된 알람: {target_time}")

    if current_time >= target_time:
        st.session_state.alarm_triggered = True

# -----------------------------
# Alarm Trigger
# -----------------------------
if st.session_state.alarm_triggered:

    st.markdown(
        """
        <div class="alarm-box">
        🚨 기상 시간입니다! 🚨<br>
        얼굴 인증 전까지 알람이 계속 울립니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    # 큰 알람음
    st.audio(
        "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3",
        autoplay=True
    )

    st.subheader("📸 세수 후 얼굴 사진 촬영")

    picture = st.camera_input(
        "얼굴을 촬영하세요"
    )

    if picture is not None:

        try:
            file_bytes = np.asarray(
                bytearray(picture.read()),
                dtype=np.uint8
            )

            image = cv2.imdecode(
                file_bytes,
                cv2.IMREAD_COLOR
            )

            gray = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY
            )

            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades +
                "haarcascade_frontalface_default.xml"
            )

            faces = face_cascade.detectMultiScale(
                gray,
                1.1,
                4
            )

            if len(faces) > 0:

                st.markdown(
                    """
                    <div class="success-box">
                    ✅ 얼굴 인증 성공!
                    <br>
                    좋은 아침입니다 ☀️
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.balloons()

                st.session_state.alarm_triggered = False
                st.session_state.alarm_active = False

            else:
                st.error(
                    "얼굴이 인식되지 않았습니다. 다시 촬영해주세요."
                )

        except Exception as e:
            st.error(
                f"이미지 처리 오류: {str(e)}"
            )
