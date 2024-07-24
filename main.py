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
st.title("지역별 인구 분석")

# 지역 선택 및 데이터 필터링
region = st.selectbox("지역을 선택하세요:", data['행정구역'].unique())
region_data = data[data['행정구역'] == region]

st.write("선택된 지역 데이터:")
st.write(region_data)

# 데이터 처리 및 시각화
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
    
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
    st.write("오류 내용:", e)

# 연령대별 인구 분포 시각화
age_groups = [
    '2024년06월_계_0세', '2024년06월_계_1세', '2024년06월_계_2세',
    '2024년06월_계_3세', '2024년06월_계_4세', '2024년06월_계_5세',
    '2024년06월_계_6세', '2024년06월_계_7세', '2024년06월_계_8세',
    '2024년06월_계_9세', '2024년06월_계_10세', '2024년06월_계_11세',
    '2024년06월_계_12세', '2024년06월_계_13세', '2024년06월_계_14세',
    '2024년06월_계_15세', '2024년06월_계_16세', '2024년06월_계_17세',
    '2024년06월_계_18세'
]

if all(col in region_data.columns for col in age_groups):
    age_population = [int(region_data[col].iloc[0].replace(",", "")) for col in age_groups]
    age_labels = [col.split('_')[-1] for col in age_groups]
    
    fig2, ax2 = plt.subplots()
    ax2.bar(age_labels, age_population, color='skyblue')
    ax2.set_xlabel('연령대')
    ax2.set_ylabel('인구수')
    ax2.set_title('연령대별 인구 분포')
    plt.xticks(rotation=90)
    st.pyplot(fig2)
else:
    st.warning("연령대별 인구 데이터가 없습니다.")

# 지역별 비교 기능
regions = st.multiselect("비교할 지역을 선택하세요:", data['행정구역'].unique())
if len(regions) > 1:
    fig3, ax3 = plt.subplots()
    for region in regions:
        region_data = data[data['행정구역'] == region]
        total_population_str = region_data['2024년06월_계_총인구수'].iloc[0]
        total_population = int(total_population_str.replace(",", ""))
        
        middle_school_population_str_13 = region_data['2024년06월_계_13세'].iloc[0]
        middle_school_population_str_14 = region_data['2024년06월_계_14세'].iloc[0]
        middle_school_population_str_15 = region_data['2024년06월_계_15세'].iloc[0]
        
        middle_school_population = (
            int(middle_school_population_str_13.replace(",", "")) +
            int(middle_school_population_str_14.replace(",", "")) +
            int(middle_school_population_str_15.replace(",", ""))
        )
        
        middle_school_percentage = (middle_school_population / total_population) * 100
        ax3.bar(region, middle_school_percentage, label=region)
    
    ax3.set_xlabel('지역')
    ax3.set_ylabel('중학생 인구 비율 (%)')
    ax3.set_title('지역별 중학생 인구 비율 비교')
    ax3.legend()
    st.pyplot(fig3)
else:
    st.warning("비교할 지역을 두 개 이상 선택하세요.")
