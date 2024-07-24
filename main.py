import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 파일 경로 및 데이터 로드
file_path = '202406_202406_연령별인구현황_월간.csv'
try:
    data = pd.read_csv(file_path, encoding='euc-kr')
except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다. 파일 경로를 확인하세요.")
    st.stop()
except Exception as e:
    st.error(f"파일 로드 중 오류가 발생했습니다: {e}")
    st.stop()

# 데이터프레임의 컬럼 이름 확인
st.write("데이터프레임 컬럼 이름:")
st.write(data.columns)

# Streamlit 앱 제목
st.title("지역별 중학생 인구 비율")

# 지역 선택
region = st.selectbox("지역을 선택하세요:", data['행정구역'].unique())

# 선택한 지역 데이터 필터링
region_data = data[data['행정구역'] == region]

st.write("선택된 지역 데이터:")
st.write(region_data)

# 데이터 처리 및 시각화
try:
    # 총 인구수 컬럼 확인
    if '2024년06월_계_총인구수' not in region_data.columns:
        st.error("총 인구수 컬럼이 데이터에 없습니다.")
        st.stop()
    
    # 중학생 인구수 컬럼 확인
    age_columns = ['2024년06월_계_13세', '2024년06월_계_14세', '2024년06월_계_15세']
    for col in age_columns:
        if col not in region_data.columns:
            st.error(f"{col} 컬럼이 데이터에 없습니다.")
            st.stop()
    
    # 총 인구수
    total_population_str = region_data['2024년06월_계_총인구수'].iloc[0]
    total_population = int(total_population_str.replace(",", ""))
    
    # 중학생 인구수
    middle_school_population_str_13 = region_data['2024년06월_계_13세'].iloc[0]
    middle_school_population_str_14 = region_data['2024년06월_계_14세'].iloc[0]
    middle_school_population_str_15 = region_data['2024년06월_계_15세'].iloc[0]
    
    middle_school_population = (
        int(middle_school_population_str_13.replace(",", "")) +
        int(middle_school_population_str_14.replace(",", "")) +
        int(middle_school_population_str_15.replace(",", ""))
    )
    
    # 인구 비율 계산
    middle_school_percentage = (middle_school_population / total_population) * 100
        
    labels = ['중학생 인구', '기타 인구']
    sizes = [middle_school_percentage, 100 - middle_school_percentage]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0)  # explode the 1st slice (i.e. 'Middle school population')

    # 파이 차트 생성
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    st.pyplot(fig1)
    
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.write("오류 내용:", e)
