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
st.title("지역별 중학생 인구 비율 및 분석")

# 지역 선택
region = st.selectbox("지역을 선택하세요:", data['행정구역'].unique())

# 선택한 지역 데이터 필터링
region_data = data[data['행정구역'] == region]

st.write("선택된 지역 데이터:")
st.write(region_data)

# 연령대 선택
age_group = st.selectbox("연령대를 선택하세요:", ['13세', '14세', '15세'])
age_column = f'2024년06월_계_{age_group}세'

if age_column not in region_data.columns:
    st.error(f"컬럼 '{age_column}'이 데이터프레임에 존재하지 않습니다. 컬럼 이름을 확인하세요.")
    st.stop()

age_population_str = region_data[age_column].iloc[0]
age_population = int(age_population_str.replace(",", ""))
st.write(f"{age_group} 인구수:", age_population)

try:
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
    
    # 막대 그래프 생성
    fig2, ax2 = plt.subplots()
    ax2.bar(['중학생 인구', '총 인구'], [middle_school_population, total_population], color=['#ff9999', '#66b3ff'])
    ax2.set_xlabel('인구 구분')
    ax2.set_ylabel('인구수')
    ax2.set_title('중학생과 총 인구 비교')
    st.pyplot(fig2)
    
    # 슬라이더를 통한 인구수 필터링
    min_pop, max_pop = st.slider(
        '인구수 범위를 선택하세요',
        min_value=0, max_value=int(total_population),
        value=(0, int(total_population))
    )
    filtered_data = region_data[
        (region_data['2024년06월_계_총인구수'].astype(int) >= min_pop) &
        (region_data['2024년06월_계_총인구수'].astype(int) <= max_pop)
    ]
    st.write("필터링된 데이터:")
    st.write(filtered_data)
    
    # 데이터 다운로드 기능
    @st.cache
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(region_data)
    st.download_button(
        label="데이터 다운로드",
        data=csv,
        file_name='region_data.csv',
        mime='text/csv',
    )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.write("오류 내용:", e)
