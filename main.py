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
st.write("날짜에 따라 영화의 일관객수가 어떻게 변하는지 알 수 있고, 관객수가 가장 많거나 적었던 시점과 전체적인 변화 추세를 확인할 수 있다.")

# ==================================================
# 앞으로 추가할 그래프 구역
# ==================================================
st.divider()

st.header("그래프 2")

st.divider()
st.header("그래프 2. 일관객 합계 상위 5편의 날짜별 일관객")
st.write("이 기간 동안 일관객 합계가 가장 큰 5편의 날짜별 일관객 변화를 비교합니다.")

# 영화별 일관객 합계 계산
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
    .tolist()
)

top5_df = df[df["영화명"].isin(top5_movies)].copy()
top5_df = top5_df.sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,.0f"
    }
)

fig2.update_traces(
    hovertemplate="영화: %{fullData.name}<br>날짜: %{x}<br>관객수: %{y:,.0f}명<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수",
    hovermode="x unified",
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.write("일관객 합계가 가장 큰 5편의 날짜별 관객수 변화를 비교할 수 있고, 영화마다 관객수가 증가하거나 감소하는 시점과 변화 폭을 확인할 수 있다.")

st.divider()

st.header("그래프 3")

st.divider()
st.header("그래프 3. 날짜별 10위권 일관객 합계")
st.write("날짜별로 그날 10위권 영화의 일관객 합계를 확인합니다.")

# 날짜별 10위권 일관객 합계 계산
daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 날 3일
top3_days = daily_total.nlargest(3, "일관객")

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,.0f"
    }
)

# 가장 큰 날 3일을 그래프 위에 표시
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers+text",
    text=[
        f"{date.strftime('%Y-%m-%d')}<br>{value:,.0f}명"
        for date, value in zip(top3_days["날짜"], top3_days["일관객"])
    ],
    textposition="top center",
    marker=dict(size=10),
    name="합계 상위 3일",
    hovertemplate="날짜: %{x}<br>합계: %{y:,.0f}명<extra></extra>"
)

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계",
    hovermode="x unified"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.write("날짜별 10위권 영화의 전체적인 관객수 변화를 확인할 수 있고, 관객수가 가장 많았던 날짜와 그날의 일관객 합계를 알 수 있다.")

st.divider()

st.header("그래프 4")

st.info("앞으로 새로운 그래프를 추가할 공간입니다.")
