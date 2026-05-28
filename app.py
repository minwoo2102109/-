import streamlit as st

# 제목
st.title("🎮 게임 코칭 앱")

# 설명
st.write("플레이 정보를 입력하면 간단한 코칭을 제공합니다.")

# 입력
game = st.text_input("게임 이름")
tier = st.selectbox(
    "현재 티어",
    ["브론즈", "실버", "골드", "플래티넘", "다이아"]
)

hours = st.slider("하루 연습 시간", 0, 10, 2)

# 버튼
if st.button("코칭 받기"):

    st.subheader("📌 코칭 결과")

    if hours < 2:
        st.success("매일 2시간 이상 꾸준히 연습해보세요.")
    else:
        st.success("좋습니다! 리플레이 분석을 추가하면 더 빨리 성장할 수 있습니다.")

    if tier == "브론즈":
        st.info("기본기와 맵 이해도를 먼저 키우세요.")
    elif tier == "실버":
        st.info("에임과 포지셔닝 연습을 추천합니다.")
    elif tier == "골드":
        st.info("팀 플레이와 운영 능력을 강화하세요.")
    else:
        st.info("상위 티어 전략 분석이 중요합니다.")

    st.write(f"🎯 {game} 코칭 완료!")
