import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('sales_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# 사이드바 필터
with st.sidebar:
    st.title('필터')
    selected_regions = st.multiselect('지역', df['region'].unique(), default=df['region'].unique())
    date_range = st.date_input('기간', value=[df['date'].min(), df['date'].max()])

# 필터 적용
df_f = df[
    df['region'].isin(selected_regions) &
    (df['date'] >= pd.Timestamp(date_range[0])) &
    (df['date'] <= pd.Timestamp(date_range[1]))
]

# KPI 카드 4개
col1, col2, col3, col4 = st.columns(4)
col1.metric('총 매출', f'₩{df_f["sales"].sum():,}', '+8.3%')
col2.metric('주문 건수', f'{len(df_f):,}건')
col3.metric('평균 주문액', f'₩{int(df_f["sales"].mean()):,}')
col4.metric('최다 판매 제품', df_f.groupby('product')['sales'].sum().idxmax())

# 탭 구성
tab1, tab2 = st.tabs(['매출 추이', '제품별 매출'])

with tab1:
    monthly = df_f.groupby('date')['sales'].sum().reset_index()
    fig = px.line(monthly, x='date', y='sales', title='일별 매출 추이')
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    product_sales = df_f.groupby('product')['sales'].sum().reset_index()
    fig2 = px.bar(product_sales, x='product', y='sales', title='제품별 매출')
    st.plotly_chart(fig2, use_container_width=True)

# 원본 데이터
with st.expander('원본 데이터'):
    st.dataframe(df_f, use_container_width=True)
