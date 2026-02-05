import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="응급병원 찾기 🏥", layout="wide")

st.title("🚑 내 주변 응급실 & 소아과 병원 찾기 🏥🧒")

# 1. 사용자 위치 입력
st.subheader("📍 현재 위치 입력")
latitude = st.number_input("위도 (예: 37.5665)", value=37.5665)
longitude = st.number_input("경도 (예: 126.9780)", value=126.9780)

# 2. 병원 데이터 (예시, 실제 데이터는 CSV 또는 API로 확장 가능)
data = {
    "병원명": ["서울종합병원", "강남어린이병원", "서초응급의료센터", "용산소아과병원"],
    "종류": ["응급", "어린이", "응급", "어린이"],
    "위도": [37.567, 37.501, 37.494, 37.532],
    "경도": [126.978, 127.028, 127.010, 126.990],
    "전화번호": ["02-111-1111", "02-222-2222", "02-333-3333", "02-444-4444"]
}
df = pd.DataFrame(data)

# 3. 지도 생성
m = folium.Map(location=[latitude, longitude], zoom_start=13)

# 내 위치 마커
folium.Marker(
    location=[latitude, longitude],
    popup="📌 내 위치",
    icon=folium.Icon(color="blue", icon="user")
).add_to(m)

# 병원 마커 추가
for idx, row in df.iterrows():
    if row['종류'] == "응급":
        icon = "🏥"
        color = "red"
    else:  # 어린이 병원
        icon = "🧸"
        color = "green"
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=f"{icon} {row['병원명']}\n📞 {row['전화번호']}",
        icon=folium.Icon(color=color, icon="plus")
    ).add_to(m)

# 4. 지도 렌더링
st.subheader("🗺️ 지도에서 확인하기")
st_data = st_folium(m, width=700, height=500)

# 5. 전화번호 리스트
st.subheader("📞 바로 전화할 수 있는 응급실 & 어린이병원")
for idx, row in df.iterrows():
    if row['종류'] == "응급":
        emoji = "🚨"
    else:
        emoji = "🧒"
    st.write(f"{emoji} {row['병원명']} - 📞 {row['전화번호']}")

# 6. 119 안내
st.info("긴급 상황 시 ☎ 119로 바로 연락하세요!")
