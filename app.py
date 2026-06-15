import streamlit as st
from streamlit_option_menu import option_menu

# ====================================================
# 페이지 설정
# ====================================================

st.set_page_config(
    page_title="유튜브 인기 요인 분석",
    page_icon="📊",
    layout="wide"
)

# ====================================================
# 사이드바
# ====================================================

with st.sidebar:

    st.markdown(
        """
        <h2 style='text-align:center;'>
        📺 YouTube
        </h2>
        <h4 style='text-align:center; color:gray;'>
        인기 요인 분석
        </h4>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    selected = option_menu(
        menu_title="Menu",

        options=[
            "프로젝트 소개",
            "데이터 탐색 (EDA)",
            "변수 검증",
            "통계 분석",
            "회귀분석",
            "Random Forest",
            "최종 결론"
        ],

        icons=[
            "house",
            "bar-chart",
            "check-circle",
            "clipboard-data",
            "graph-up",
            "tree",
            "flag"
        ],

        menu_icon="cast",
        default_index=0,

        styles={

            "container": {
                "padding": "10px",
                "background-color": "#f8f9fa",
                "border-radius": "15px"
            },

            "icon": {
                "color": "#1f2937",
                "font-size": "18px"
            },

            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px",
                "padding": "12px",
                "--hover-color": "#e5e7eb",
                "border-radius": "10px"
            },

            "nav-link-selected": {
                "background-color": "#14b8a6",
                "color": "white",
                "border-radius": "10px"
            },

            "menu-title": {
                "font-size": "22px",
                "font-weight": "bold"
            }
        }
    )

# ====================================================
# 페이지 내용
# ====================================================

if selected == "프로젝트 소개":

    st.title("📊 유튜브 인기 요인 분석")

    st.header("연구 주제")

    st.write("""
    유튜브 영상의 조회수는 좋아요 수, 댓글 수,
    제목 길이, 업로드 시점과 같은 다양한 요소들과
    어떠한 관계를 보이는가?
    """)

    st.header("데이터 개요")

    col1, col2, col3 = st.columns(3)

    col1.metric("영상 수", "4,183개")
    col2.metric("카테고리", "5개")
    col3.metric("분석 변수", "10개")

# ====================================================

elif selected == "데이터 탐색 (EDA)":

    st.title("📈 데이터 탐색 (EDA)")

    st.subheader("조회수 분포")

    st.info("로그 변환 전후 조회수 분포 그래프 표시 예정")

    st.subheader("카테고리 분포")

    st.info("카테고리별 영상 수 그래프 표시 예정")

# ====================================================

elif selected == "변수 검증":

    st.title("✅ 변수 검증")

    st.subheader("얼굴 인식 검증")

    col1, col2 = st.columns(2)

    col1.metric("Accuracy", "68%")
    col2.metric("Precision", "96.7%")

    col1.metric("Recall", "65.9%")
    col2.metric("F1-score", "78.4%")

    st.divider()

    st.subheader("카테고리 검증")

    st.metric("전체 정확도", "92%")

    st.table({
        "카테고리": ["music", "mukbang", "news", "asmr", "vlog"],
        "정확도": ["90%", "80%", "100%", "90%", "100%"]
    })

# ====================================================

elif selected == "통계 분석":

    st.title("📋 통계 분석")

    st.subheader("Welch's t-test")

    st.metric("p-value", "0.102")

    st.error("유의한 차이 없음")

    st.divider()

    st.subheader("Mann-Whitney U Test")

    st.metric("p-value", "0.248")

    st.error("유의한 차이 없음")

    st.success(
        "얼굴 포함 여부는 조회수에 통계적으로 유의한 영향을 주지 않음"
    )

# ====================================================

elif selected == "회귀분석":

    st.title("📉 회귀분석")

    st.subheader("부분상관분석")

    st.table({
        "분석": [
            "단순상관",
            "구독자 수 통제",
            "업로드 시간 통제",
            "둘 다 통제"
        ],
        "상관계수": [
            "-0.066",
            "-0.109",
            "-0.139",
            "-0.197"
        ]
    })

    st.divider()

    st.subheader("다중회귀분석")

    st.table({
        "변수": [
            "좋아요 수",
            "댓글 수",
            "구독자 수",
            "태그 수"
        ],
        "계수": [
            "+0.280",
            "+0.173",
            "+0.074",
            "-0.013"
        ]
    })

# ====================================================

elif selected == "Random Forest":

    st.title("🌲 Random Forest")

    st.metric("R² Score", "0.832")

    st.subheader("변수 중요도")

    st.table({
        "변수": [
            "좋아요 수",
            "구독자 수",
            "댓글 수",
            "업로드 경과 시간",
            "태그 수"
        ],
        "중요도": [
            "75.4%",
            "8.7%",
            "6.1%",
            "5.0%",
            "1.6%"
        ]
    })

# ====================================================

elif selected == "최종 결론":

    st.title("🎯 최종 결론")

    st.success("""
    조회수에 가장 큰 영향을 미치는 변수는
    좋아요 수였다.
    """)

    st.subheader("조회수 영향 순위")

    st.write("""
    🥇 좋아요 수

    🥈 구독자 수

    🥉 댓글 수

    4️⃣ 업로드 경과 시간
    """)

    st.divider()

    st.subheader("영향이 거의 없는 변수")

    st.write("""
    • 얼굴 포함 여부

    • 숫자 포함 여부

    • 감성어 포함 여부
    """)
