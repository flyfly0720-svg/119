import streamlit as st
import pandas as pd
import math

# 🎨 페이지 설정
st.set_page_config(
    page_title="🚑 응급실 찾기 앱",
    page_icon="🏥",
    layout="centered"
)

st.title("🚑 가까운 응급실 찾기 앱 🏥")
st.write("💡 **내가 사는 지역에서 가장 가까운 병원과 전화번호를 알려드려요!**")

# 📍 병원 데이터 (예시, 오류 없음)
data = [
    {"지역": "서울", "병원명": "서울중앙병원", "위도": 37.5665, "경도": 126.9780, "전화번호": "02-123-4567", "소아과": False},
    {"지역": "서울", "병원명": "서울어린이병원", "위도": 37.5700, "경도": 126.9820, "전화번호": "02-777-8888", "소아과": True},

    {"지역": "부산", "병원명": "부산의료원", "위도": 35.1796, "경도": 129.0756, "전화번호": "051-222-3333", "소아과": False},
    {"지역": "부산", "병원명": "부산소아병원", "위도": 35.1800, "경도": 129.0800, "전화번호": "051-999-0000", "소아과": True},

    {"지역": "대구", "병원명": "대구응급센터", "위도": 35.8714, "경도": 128.6014, "전화번호": "053-111-2222", "소아과": False},
    {"지역": "대구", "병원명": "대구아이병원", "위도": 35.8720, "경도": 128.6050, "전화번호": "053-333-4444", "소아과": True},
]

df = pd.DataFrame(data)

# 🏠 지역 선택
region = st.selectbox("🏠 거주 지역을 선택하세요", df["지역"].unique())

# 📌 기준 좌표 (지역 중심)
region_center = {
    "서울": (37.5665, 126.9780),
    "부산": (35.1796, 129.0756),
    "대구": (35.8714, 128.6014),
}

# 📐 거리 계산 함수
def calc_distance(lat1, lon1, lat2, lon2):
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

# 🔍 선택한 지역 병원 필터
user_lat, user_lon = region_center[region]
region_df = df[df["지역"] == region].copy()

region_df["거리"] = region_df.apply(
    lambda row: calc_distance(user_lat, user_lon, row["위도"], row["경도"]),
    axis=1
)

# 🚑 가장 가까운 응급실
er_df = region_df[region_df["소아과"] == False].sort_values("거리")
nearest_er = er_df.iloc[0]

st.subheader("🚨 가장 가까운 응급실 🏥")
st.success(f"""
🏥 **병원명**: {nearest_er['병원명']}  
📞 **전화번호**: {nearest_er['전화번호']}  
📍 **거리**: 매우 가까움 😆  
""")

# 👶 소아과 따로 표시
st.subheader("👶 소아과 병원 목록 🧸")
pediatric_df = region_df[region_df["소아과"] == True]

for _, row in pediatric_df.iterrows():
    st.info(f"""
👶 **병원명**: {row['병원명']}  
📞 **전화번호**: {row['전화번호']}  
💖 아이들을 위한 병원이에요!
""")

st.markdown("---")
st.caption("⚠️ 실제 응급 상황에서는 반드시 119에 먼저 연락하세요 🚑🔥")



