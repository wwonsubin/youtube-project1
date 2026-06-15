import streamlit as st

st.set_page_config(
    page_title="유튜브 인기 요인 분석",
    page_icon="📊",
    layout="wide"
)

# =====================
# 사이드바
# =====================

menu = st.sidebar.radio(
    "메뉴 선택",
    [
        "프로젝트 소개",
        "데이터 탐색 (EDA)",
        "변수 검증",
        "통계 분석",
        "회귀분석",
        "Random Forest",
        "최종 결론"
    ]
)

# =====================
# 페이지별 화면
# =====================

if menu == "프로젝트 소개":

    st.title("📊 유튜브 인기 요인 분석")

    st.header("연구 주제")

    st.write("""
    유튜브 조회수에 영향을 미치는 다양한 요인을 분석하고,
    인기 영상의 공통적인 특징을 파악한다.
    """)

elif menu == "데이터 탐색 (EDA)":

    st.title("📈 데이터 탐색")

    st.write("조회수 분포")
    st.write("카테고리 분포")

elif menu == "변수 검증":

    st.title("✅ 변수 검증")

    st.subheader("얼굴 인식 검증")

    st.write("Accuracy : 68%")
    st.write("Precision : 96.7%")
    st.write("Recall : 65.9%")
    st.write("F1-score : 78.4%")

    st.subheader("카테고리 검증")

    st.write("전체 정확도 : 92%")

elif menu == "통계 분석":

    st.title("📊 통계 분석")

    st.subheader("t-test")

    st.write("p-value = 0.102")

    st.subheader("Mann-Whitney U Test")

    st.write("p-value = 0.248")

elif menu == "회귀분석":

    st.title("📉 회귀분석")

    st.write("부분상관분석")
    st.write("다중회귀분석")

elif menu == "Random Forest":

    st.title("🌲 Random Forest")

    st.write("변수 중요도 분석")

elif menu == "최종 결론":

    st.title("🎯 최종 결론")

    st.write("""
    좋아요 수 > 구독자 수 > 댓글 수 > 업로드 경과 시간
    """)

    st.write("""
    얼굴 포함 여부, 숫자 포함 여부,
    감성어 포함 여부는 영향이 거의 없었다.
    """)
