import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize-matplotlib

# Load data
file_path = '202406_202406_연령별인구현황_월간.csv'
data = pd.read_csv(file_path, encoding='cp949')

# Streamlit App
st.title('지역별 중학생 인구 비율')

# 지역 선택
region = st.selectbox('지역을 선택하세요:', data['행정구역'].unique())

# 선택한 지역의 데이터 필터링
region_data = data[data['행정구역'] == region]

# 중학생 인구 (13세 ~ 15세) 합계
middle_school_population = region_data[['2024년06월_계_13세', '2024년06월_계_14세', '2024년06월_계_15세']].astype(int).sum(axis=1).values[0]

# 전체 인구
total_population = region_data['2024년06월_계_총인구수'].astype(int).values[0]

# 비율 계산
middle_school_ratio = middle_school_population / total_population * 100
others_ratio = 100 - middle_school_ratio

# 데이터 준비
labels = ['중학생 인구 비율', '기타 인구 비율']
sizes = [middle_school_ratio, others_ratio]
colors = ['#ff9999','#66b3ff']
explode = (0.1, 0)  # 중학생 인구 비율을 강조

# 원 그래프 그리기
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# 그래프 출력
st.pyplot(fig1)
