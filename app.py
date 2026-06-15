import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ====================================================
# 페이지 설정
# ====================================================

st.set_page_config(
    page_title="유튜브 인기 요인 분석",
    page_icon="📊",
    layout="wide"
)

# ====================================================
# 데이터 불러오기
# ====================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/youtube_final_dataset.csv", encoding="utf-8-sig")

    df["log_view_count"] = np.log1p(df["view_count"])

    return df

df = load_data()

# ====================================================
# 사이드바
# ====================================================

with st.sidebar:

    st.markdown(
        """
        <h2 style='text-align:center;'>📺 YouTube</h2>
        <h4 style='text-align:center; color:gray;'>인기 요인 분석</h4>
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
# 1. 프로젝트 소개
# ====================================================

if selected == "프로젝트 소개":

    st.title("📊 유튜브 인기 요인 분석")

    st.markdown("""
    본 프로젝트는 유튜브 영상의 조회수에 영향을 미치는 요인을 분석하기 위해 수행되었다.  
    단순히 조회수와 좋아요 수의 관계만 확인하는 것이 아니라, 댓글 수, 구독자 수, 태그 수, 제목 특성, 썸네일 인물 포함 여부 등 다양한 변수를 함께 고려하였다.
    """)

    st.header("연구 주제")

    st.info("""
    유튜브 영상의 조회수는 좋아요 수, 댓글 수, 제목 길이, 업로드 시점, 태그 수, 썸네일 인물 포함 여부 등과 어떤 관계를 보이는가?
    """)

    st.header("데이터 수집 방법")

    st.markdown("""
    - **YouTube Data API**를 활용하여 영상 데이터를 수집하였다.
    - 수집 항목은 영상 제목, 채널명, 업로드 날짜, 조회수, 좋아요 수, 댓글 수, 태그 수, 썸네일 URL 등이다.
    - 추가적으로 채널 규모를 통제하기 위해 **채널 구독자 수**를 추가 수집하였다.
    - OpenCV Haar Cascade를 활용하여 썸네일에 인물이 포함되어 있는지 여부를 `has_person` 변수로 생성하였다.
    - 제목 기반 변수로 숫자 포함 여부, 특수문자 개수, 감성어 포함 여부를 생성하였다.
    """)

    st.header("데이터 개요")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("전체 영상 수", f"{len(df):,}개")
    col2.metric("카테고리 수", f"{df['category'].nunique()}개")
    col3.metric("채널 수", f"{df['channel_title'].nunique():,}개")
    col4.metric("평균 조회수", f"{df['view_count'].mean():,.0f}")

    st.subheader("분석 카테고리")

    st.markdown("""
    본 프로젝트에서는 다음 5개 카테고리를 대상으로 분석하였다.

    - **music**: 음악, 노래, 무대 영상
    - **mukbang**: 먹방, 음식 리뷰, 식사 콘텐츠
    - **news**: 뉴스, 시사, 이슈 관련 영상
    - **asmr**: ASMR, 수면, 힐링 사운드 콘텐츠
    - **vlog**: 일상 브이로그, 생활 기록형 콘텐츠
    """)

    category_count = df["category"].value_counts().reset_index()
    category_count.columns = ["category", "count"]

    st.subheader("카테고리별 영상 수")

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=category_count, x="category", y="count", ax=ax)
    ax.set_title("Category Count")
    ax.set_xlabel("Category")
    ax.set_ylabel("Video Count")
    st.pyplot(fig)

    st.dataframe(category_count, use_container_width=True)

# ====================================================
# 2. 데이터 탐색
# ====================================================

elif selected == "데이터 탐색 (EDA)":

    st.title("📈 데이터 탐색 (EDA)")

    st.markdown("""
    EDA 단계에서는 조회수의 분포, 카테고리별 조회수 차이, 로그 변환 전후의 분포 변화를 확인하였다.  
    유튜브 조회수 데이터는 일부 초대형 영상으로 인해 매우 강한 우편향을 보이기 때문에, 분석 단계에서는 로그 변환을 함께 사용하였다.
    """)

    st.header("조회수 기초 통계")

    col1, col2, col3 = st.columns(3)

    col1.metric("평균 조회수", f"{df['view_count'].mean():,.0f}")
    col2.metric("중앙값 조회수", f"{df['view_count'].median():,.0f}")
    col3.metric("최대 조회수", f"{df['view_count'].max():,.0f}")

    st.markdown("""
    평균 조회수가 중앙값보다 크게 나타난 것은 일부 영상의 조회수가 매우 높아 전체 평균을 끌어올렸기 때문이다.
    """)

    st.subheader("원본 조회수 분포")

    fig, ax = plt.subplots(figsize=(9, 4))
    sns.histplot(df["view_count"], bins=50, ax=ax)
    ax.set_title("View Count Distribution")
    ax.set_xlabel("View Count")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    st.subheader("원본 조회수 박스플롯")

    fig, ax = plt.subplots(figsize=(9, 2.5))
    sns.boxplot(x=df["view_count"], ax=ax)
    ax.set_title("View Count Boxplot")
    st.pyplot(fig)

    st.markdown("""
    원본 조회수 분포는 극단적으로 오른쪽으로 치우쳐 있으며, 박스플롯에서도 이상치가 많이 나타났다.  
    따라서 단순 평균 비교만으로 결론을 내리기에는 한계가 있다.
    """)

    st.subheader("로그 변환 후 조회수 분포")

    fig, ax = plt.subplots(figsize=(9, 4))
    sns.histplot(df["log_view_count"], bins=50, ax=ax)
    ax.set_title("Log(View Count) Distribution")
    ax.set_xlabel("Log(View Count)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    st.subheader("로그 변환 후 박스플롯")

    fig, ax = plt.subplots(figsize=(9, 2.5))
    sns.boxplot(x=df["log_view_count"], ax=ax)
    ax.set_title("Log(View Count) Boxplot")
    st.pyplot(fig)

    st.success("""
    로그 변환 후 분포가 원본보다 안정적으로 변했기 때문에, 회귀분석과 모델링에서는 `log_view_count`를 종속변수로 사용하였다.
    """)

    st.header("카테고리별 평균 조회수")

    cat_view = df.groupby("category")["view_count"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=cat_view, x="category", y="view_count", ax=ax)
    ax.set_title("Average View Count by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Average View Count")
    st.pyplot(fig)

    st.header("카테고리별 로그 조회수 분포")

    fig, ax = plt.subplots(figsize=(9, 4))
    sns.boxplot(data=df, x="category", y="log_view_count", ax=ax)
    ax.set_title("Log View Count by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Log View Count")
    st.pyplot(fig)

# ====================================================
# 3. 변수 검증
# ====================================================

elif selected == "변수 검증":

    st.title("✅ 변수 검증")

    st.markdown("""
    교수님 피드백을 반영하여, 분석에 사용한 주요 변수들이 신뢰할 수 있는지 검증하였다.  
    특히 OpenCV로 생성한 얼굴 인식 변수와 검색어 기반 카테고리 분류의 정확도를 수동 검수로 확인하였다.
    """)

    st.header("1. 얼굴 인식 검증")

    st.markdown("""
    OpenCV Haar Cascade를 활용하여 썸네일에 인물이 포함되어 있는지 여부를 `has_person` 변수로 생성하였다.  
    그러나 자동 인식 결과가 항상 정확하다고 볼 수 없기 때문에, 무작위 50개 썸네일을 수동 검수하여 실제 얼굴 포함 여부와 비교하였다.
    """)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Accuracy", "68.0%")
    col2.metric("Precision", "96.7%")
    col3.metric("Recall", "65.9%")
    col4.metric("F1-score", "78.4%")

    st.markdown("""
    - **Precision이 높다**는 것은 OpenCV가 얼굴이 있다고 판단한 경우 실제로 얼굴이 있을 가능성이 높다는 의미이다.
    - **Recall이 낮다**는 것은 실제 얼굴이 있음에도 탐지하지 못한 경우가 일부 있었다는 의미이다.
    - 따라서 `has_person` 변수는 활용 가능하지만, 일부 얼굴을 놓치는 한계가 존재한다.
    """)

    st.subheader("Confusion Matrix")

    cm = pd.DataFrame(
        [[5, 1], [15, 29]],
        index=["실제 얼굴 없음", "실제 얼굴 있음"],
        columns=["예측 얼굴 없음", "예측 얼굴 있음"]
    )

    st.dataframe(cm, use_container_width=True)

    st.header("2. 카테고리 검증")

    st.markdown("""
    카테고리는 검색 키워드를 기반으로 수집되었기 때문에, 실제 영상 내용이 해당 카테고리와 일치하는지 검증할 필요가 있었다.  
    이에 따라 각 카테고리별로 표본을 추출하여 수동 검수하였다.
    """)

    st.metric("전체 카테고리 정확도", "92%")

    category_acc = pd.DataFrame({
        "category": ["asmr", "mukbang", "music", "news", "vlog"],
        "accuracy": [0.9, 0.8, 0.9, 1.0, 1.0]
    })

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=category_acc, x="category", y="accuracy", ax=ax)
    ax.set_ylim(0, 1.1)
    ax.set_title("Category Validation Accuracy")
    ax.set_xlabel("Category")
    ax.set_ylabel("Accuracy")
    st.pyplot(fig)

    st.dataframe(category_acc, use_container_width=True)

    st.markdown("""
    전체 정확도는 92%로 나타났으며, 검색어 기반 카테고리 분류가 전반적으로 신뢰 가능한 수준임을 확인하였다.  
    다만 먹방 카테고리는 음식 리뷰, 일상 브이로그 등이 일부 섞여 상대적으로 정확도가 낮게 나타났다.
    """)

# ====================================================
# 4. 통계 분석
# ====================================================

elif selected == "통계 분석":

    st.title("📋 통계 분석")

    st.markdown("""
    얼굴 포함 썸네일이 조회수에 영향을 미치는지 확인하기 위해 얼굴 포함 영상과 미포함 영상의 조회수 차이를 검정하였다.  
    조회수 데이터는 강한 우편향을 보였기 때문에 Welch's t-test와 Mann-Whitney U Test를 함께 수행하였다.
    """)

    st.header("검정 결과")

    result_test = pd.DataFrame({
        "검정 방법": ["Welch's t-test", "Mann-Whitney U Test"],
        "p-value": [0.1019, 0.2480],
        "결론": ["유의하지 않음", "유의하지 않음"]
    })

    st.dataframe(result_test, use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric("Welch's t-test p-value", "0.1019")
    col2.metric("Mann-Whitney p-value", "0.2480")

    st.warning("""
    두 검정 모두 p-value가 0.05보다 크므로 얼굴 포함 여부에 따른 조회수 차이는 통계적으로 유의하지 않았다.
    """)

    st.subheader("얼굴 포함 여부별 로그 조회수 분포")

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.boxplot(data=df, x="has_person", y="log_view_count", ax=ax)
    ax.set_xticklabels(["No Face", "Face"])
    ax.set_title("Face vs No Face (Log Views)")
    ax.set_xlabel("Thumbnail Face")
    ax.set_ylabel("Log View Count")
    st.pyplot(fig)

    st.markdown("""
    박스플롯에서도 두 집단의 중앙값과 분포 차이가 크지 않음을 확인할 수 있다.  
    따라서 얼굴이 포함된 썸네일이 조회수를 높인다고 단정하기 어렵다.
    """)

# ====================================================
# 5. 회귀분석
# ====================================================

elif selected == "회귀분석":

    st.title("📉 회귀분석")

    st.markdown("""
    단순 상관관계만으로는 변수 간 관계를 정확히 해석하기 어렵다.  
    따라서 구독자 수와 업로드 후 경과 시간 같은 잠복변수를 통제한 부분상관분석과 다중회귀분석을 수행하였다.
    """)

    st.header("1. 부분상관분석")

    partial_corr = pd.DataFrame({
        "분석": [
            "단순상관",
            "구독자 수 통제",
            "업로드 경과 시간 통제",
            "구독자 수 + 업로드 경과 시간 통제"
        ],
        "상관계수": [-0.0658, -0.1086, -0.1392, -0.1965],
        "p-value": [
            "0.0014",
            "1.24e-07",
            "1.12e-11",
            "5.92e-22"
        ]
    })

    st.dataframe(partial_corr, use_container_width=True)

    fig, ax = plt.subplots(figsize=(9, 4))
    sns.barplot(data=partial_corr, x="분석", y="상관계수", ax=ax)
    ax.set_title("Partial Correlation: Tag Count vs Log View Count")
    ax.set_xlabel("Control Variables")
    ax.set_ylabel("Correlation")
    ax.tick_params(axis="x", rotation=20)
    st.pyplot(fig)

    st.markdown("""
    태그 수와 조회수는 단순 상관에서도 약한 음의 관계를 보였으며, 구독자 수와 업로드 경과 시간을 통제한 이후에도 음의 관계가 유지되었다.  
    이는 태그 수가 많을수록 조회수가 낮다는 단순 해석보다는, 태그를 많이 사용하는 영상의 특성이 다를 가능성을 함께 고려해야 함을 의미한다.
    """)

    st.header("2. 다중회귀분석")

    reg_result = pd.DataFrame({
        "변수": [
            "log_like_count",
            "log_comment_count",
            "log_subscriber_count",
            "log_days_since_upload",
            "tag_count",
            "title_length",
            "has_person",
            "has_number",
            "special_char_count",
            "has_emotion_word"
        ],
        "계수": [
            0.279977,
            0.173428,
            0.074363,
            0.401550,
            -0.013235,
            0.009021,
            -0.010045,
            -0.461415,
            -0.017824,
            -0.408250
        ],
        "p-value": [
            "1.44e-113",
            "4.13e-31",
            "2.63e-08",
            "2.44e-69",
            "1.57e-16",
            "6.99e-14",
            "0.849",
            "5.99e-10",
            "0.00061",
            "2.43e-06"
        ]
    })

    st.dataframe(reg_result, use_container_width=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=reg_result, x="계수", y="변수", ax=ax)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_title("Regression Coefficients")
    ax.set_xlabel("Coefficient")
    ax.set_ylabel("Variable")
    st.pyplot(fig)

    st.success("""
    회귀분석 결과 좋아요 수, 댓글 수, 구독자 수, 업로드 경과 시간은 조회수와 양의 관계를 보였다.  
    반면 태그 수, 숫자 포함 여부, 감성어 포함 여부는 음의 관계를 보였다.  
    얼굴 포함 여부는 통계적으로 유의하지 않았다.
    """)

# ====================================================
# 6. Random Forest
# ====================================================

elif selected == "Random Forest":

    st.title("🌲 Random Forest")

    st.markdown("""
    다중회귀분석은 변수의 방향성과 통계적 유의성을 확인하는 데 유용하지만, 선형 관계를 가정한다는 한계가 있다.  
    이에 따라 Random Forest 모델을 추가로 사용하여 조회수 예측에 기여하는 변수 중요도를 분석하였다.
    """)

    col1, col2, col3 = st.columns(3)

    col1.metric("MAE", "0.4695")
    col2.metric("RMSE", "0.6603")
    col3.metric("R²", "0.8318")

    st.markdown("""
    R² 값은 0.8318로 나타났으며, 이는 모델이 로그 조회수 변동의 약 83.2%를 설명한다는 의미이다.
    """)

    importance_df = pd.DataFrame({
        "feature": [
            "log_like_count",
            "log_subscriber_count",
            "log_comment_count",
            "log_days_since_upload",
            "tag_count",
            "title_length",
            "special_char_count",
            "has_person",
            "has_number",
            "has_emotion_word"
        ],
        "importance": [
            0.753781,
            0.087480,
            0.060867,
            0.050267,
            0.016209,
            0.016037,
            0.011315,
            0.001971,
            0.001463,
            0.000611
        ]
    })

    st.subheader("변수 중요도")

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=importance_df, x="importance", y="feature", ax=ax)
    ax.set_title("Random Forest Feature Importance")
    ax.set_xlabel("Importance")
    ax.set_ylabel("Feature")
    st.pyplot(fig)

    st.dataframe(importance_df, use_container_width=True)

    st.success("""
    Random Forest 분석 결과 조회수 예측에 가장 중요한 변수는 좋아요 수로 나타났다.  
    그 다음으로 구독자 수, 댓글 수, 업로드 경과 시간이 중요한 변수로 확인되었다.  
    반면 얼굴 포함 여부, 숫자 포함 여부, 감성어 포함 여부는 예측 중요도가 매우 낮았다.
    """)

# ====================================================
# 7. 최종 결론
# ====================================================

elif selected == "최종 결론":

    st.title("🎯 최종 결론")

    st.header("핵심 결과 요약")

    st.markdown("""
    본 프로젝트는 유튜브 인기 영상의 조회수에 영향을 미치는 요인을 분석하기 위해 데이터 수집, 전처리, 변수 검증, 통계 분석, 회귀분석, Random Forest 모델링을 수행하였다.
    """)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("1위", "좋아요 수")
    col2.metric("2위", "구독자 수")
    col3.metric("3위", "댓글 수")
    col4.metric("4위", "업로드 경과 시간")

    st.subheader("조회수에 강한 관련성을 보인 변수")

    st.markdown("""
    - **좋아요 수**: 조회수 예측에서 가장 높은 중요도를 보였다.
    - **구독자 수**: 채널 규모를 나타내는 중요한 잠복변수로 확인되었다.
    - **댓글 수**: 시청자 반응을 나타내는 지표로 조회수와 밀접한 관련이 있었다.
    - **업로드 경과 시간**: 시간이 지날수록 조회수가 누적되는 특성을 반영하였다.
    """)

    st.subheader("영향이 제한적인 변수")

    st.markdown("""
    - **태그 수**: 통계적으로 유의한 음의 관계를 보였지만, Random Forest 중요도는 낮았다.
    - **제목 길이**: 회귀분석에서는 유의했으나 예측 중요도는 제한적이었다.
    - **특수문자 사용**: 조회수 예측에 큰 영향을 주지는 않았다.
    """)

    st.subheader("영향이 거의 없었던 변수")

    st.markdown("""
    - **썸네일 얼굴 포함 여부**
    - **제목 숫자 포함 여부**
    - **제목 감성어 포함 여부**
    """)

    st.success("""
    최종적으로 유튜브 조회수는 제목이나 썸네일의 단순한 형식적 요소보다,
    좋아요 수, 댓글 수, 구독자 수와 같은 시청자 반응 및 채널 규모와 더 강한 관련성을 보였다.
    """)

    st.warning("""
    단, 좋아요 수와 댓글 수는 조회수의 원인이라기보다 조회수와 함께 증가하는 사후 반응 지표일 수 있다.  
    따라서 본 연구 결과는 인과관계가 아니라 관련성과 예측 중요도를 중심으로 해석해야 한다.
    """)
