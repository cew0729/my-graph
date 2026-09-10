import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")

st.write("365일 동안의 일별 박스오피스 10위권 데이터를 이용해 영화의 관객수 변화를 살펴봅니다.")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자 열을 숫자형으로 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.error(str(e))
    st.stop()


# --------------------------------------------------
# 데이터 정보
# --------------------------------------------------
st.info(
    f"📊 전체 데이터: {len(df):,}개 기록 | "
    f"📅 기간: {df['날짜'].min().strftime('%Y-%m-%d')} ~ "
    f"{df['날짜'].max().strftime('%Y-%m-%d')}"
)


# ==================================================
# 그래프 1. 영화별 일관객 변화
# ==================================================
st.header("그래프 1. 영화별 일관객 변화")

st.write("영화를 선택하면 해당 영화의 날짜별 일관객 변화를 확인할 수 있습니다.")


# 영화 목록
movie_list = sorted(
    df["영화명"].dropna().unique().tolist()
)

selected_movie = st.selectbox(
    "영화를 선택하세요",
    movie_list
)


# 선택한 영화 데이터
movie_df = df[df["영화명"] == selected_movie].copy()

movie_df = movie_df.sort_values("날짜")


# 선 그래프
fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,.0f"
    }
)

fig.update_traces(
    hovertemplate="날짜: %{x}<br>관객수: %{y:,.0f}명<extra></extra>"
)

fig.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# 그래프 설명 작성 공간
st.markdown("**이 그래프로 알 수 있는 것**")

st.text_area(
    "직접 작성하세요.",
    placeholder="날짜에 따라 영화의 일관객수가 어떻게 변하는지 알 수 있고, 관객수가 가장 많거나 적었던 시점과 전체적인 변화 추세를 확인할 수 있다.",
    key="graph1_description"
)


# ==================================================
# 앞으로 추가할 그래프 구역
# ==================================================
st.divider()

st.header("그래프 2")

st.info("앞으로 새로운 그래프를 추가할 공간입니다.")


st.divider()

st.header("그래프 3")

st.info("앞으로 새로운 그래프를 추가할 공간입니다.")


st.divider()

st.header("그래프 4")

st.info("앞으로 새로운 그래프를 추가할 공간입니다.")
