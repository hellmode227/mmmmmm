import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize-matplotlib

# Load the CSV file with 'euc-kr' encoding
file_path = '202406_202406_연령별인구현황_월간.csv'
data = pd.read_csv(file_path, encoding='euc-kr')

# Streamlit app
st.title("지역별 중학생 인구 비율")

# Select a region
region = st.selectbox("지역을 선택하세요:", data['행정구역'].unique())

# Filter the data for the selected region
region_data = data[data['행정구역'] == region]

# Calculate the total population and middle school age population (13-15 years old)
total_population = int(region_data['2024년06월_계_총인구수'].iloc[0].replace(",", ""))
middle_school_population = (
    int(region_data['2024년06월_계_13세'].iloc[0].replace(",", "")) +
    int(region_data['2024년06월_계_14세'].iloc[0].replace(",", "")) +
    int(region_data['2024년06월_계_15세'].iloc[0].replace(",", ""))
)

# Calculate the percentage
middle_school_percentage = (middle_school_population / total_population) * 100

# Create a pie chart
labels = ['중학생 인구', '기타 인구']
sizes = [middle_school_percentage, 100 - middle_school_percentage]
colors = ['#ff9999', '#66b3ff']
explode = (0.1, 0)  # explode the 1st slice (i.e. 'Middle school population')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Display the pie chart
st.pyplot(fig1)
