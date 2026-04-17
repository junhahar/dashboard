import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv('sales_data.csv')
df['date'] = pd.to_datetime(df['date'])
# KPI 카드 4개
col1, col2, col3, col4 = st.columns(4)
col1.metric('총 매출', f'₩{df["sales"].sum():,}', '+8.3%')
# TODO: col2, col3, col4 에 주문수 / 평균 주문액 / 최다 판매 제품 추가
# 탭 구성
tab1, tab2 = st.tabs([' 매출 추이', ' 제품별 매출'])
with tab1:
	monthly = df.groupby('date')['sales'].sum().reset_index()
	fig = px.line(monthly, x='date', y='sales', title='일별 매출 추이')
	st.plotly_chart(fig, use_container_width=True)
with tab2:
	# TODO: 제품별 막대 차트 추가
	pass
# 원본 데이터 expander
with st.expander('원본 데이터'):
	st.dataframe(df, use_container_width=True)