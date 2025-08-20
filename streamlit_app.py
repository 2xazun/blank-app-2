# app.py
import streamlit as st
import pandas as pd
import numpy as np

# -------------------- 페이지 설정 --------------------
# 페이지의 제목, 아이콘, 레이아웃을 설정합니다.
# 'wide' 레이아웃은 콘텐츠가 화면 전체 너비를 사용하도록 합니다.
st.set_page_config(
    page_title="인터랙티브 데이터 대시보드",
    page_icon="📊",
    layout="wide",
)

# -------------------- 데이터 캐싱 --------------------
# Streamlit의 캐싱 기능을 사용하여 데이터 로딩과 같은
# 비용이 많이 드는 작업을 최적화합니다.
# 한번 로드된 데이터는 입력 매개변수가 변경되지 않는 한 다시 로드되지 않습니다.
@st.cache_data
def load_data():
    """
    샘플 데이터프레임을 생성하고 반환하는 함수입니다.
    실제 애플리케이션에서는 이 부분에서 CSV 파일이나 데이터베이스에서 데이터를 로드할 수 있습니다.
    """
    data = pd.DataFrame({
        '카테고리': np.random.choice(['A', 'B', 'C'], 100),
        '값': np.random.randn(100).cumsum(),
        '날짜': pd.to_datetime(pd.date_range('2023-01-01', periods=100, freq='D'))
    })
    return data

# -------------------- 사이드바 --------------------
# st.sidebar를 사용하여 모든 컨트롤을 사이드바에 배치합니다.
# 이는 메인 콘텐츠 영역을 깔끔하게 유지하는 데 도움이 됩니다.
with st.sidebar:
    st.header("필터 옵션")

    # 데이터 로드
    df = load_data()

    # 카테고리 필터
    # 멀티셀렉트 위젯을 사용하여 사용자가 하나 이상의 카테고리를 선택할 수 있도록 합니다.
    selected_categories = st.multiselect(
        "카테고리 선택",
        options=df['카테고리'].unique(),
        default=df['카테고리'].unique()
    )

    # 날짜 범위 필터
    # 날짜 입력 위젯을 사용하여 사용자가 날짜 범위를 선택할 수 있도록 합니다.
    start_date = st.date_input(
        "시작 날짜",
        value=df['날짜'].min(),
        min_value=df['날짜'].min(),
        max_value=df['날짜'].max()
    )
    end_date = st.date_input(
        "종료 날짜",
        value=df['날짜'].max(),
        min_value=df['날짜'].min(),
        max_value=df['날짜'].max()
    )

# -------------------- 데이터 필터링 --------------------
# 사용자가 사이드바에서 선택한 옵션을 기반으로 데이터프레임을 필터링합니다.
# 필터링된 데이터는 새로운 변수에 저장됩니다.
filtered_df = df[
    (df['카테고리'].isin(selected_categories)) &
    (pd.to_datetime(df['날짜']).dt.date >= start_date) &
    (pd.to_datetime(df['날짜']).dt.date <= end_date)
]

# -------------------- 메인 페이지 --------------------
st.title("📊 인터랙티브 데이터 대시보드")
st.write("사이드바의 필터를 사용하여 데이터를 탐색해보세요.")

# 메트릭 표시
# st.columns를 사용하여 레이아웃을 여러 열로 나눕니다.
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="총 데이터 수", value=len(filtered_df))
with col2:
    st.metric(label="평균 값", value=f"{filtered_df['값'].mean():.2f}")
with col3:
    st.metric(label="최대 값", value=f"{filtered_df['값'].max():.2f}")

st.markdown("---")

# 필터링된 데이터 테이블 표시
st.subheader("필터링된 데이터")
st.dataframe(filtered_df)

# 라인 차트 시각화
st.subheader("시간에 따른 값의 변화")
st.line_chart(filtered_df.set_index('날짜')['값'])