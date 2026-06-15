import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

st.title("유튜브 인기 요인 분석")

st.header("현재 Google Trends 인기 검색어")

def get_google_trends():
    url = "https://trends.google.com/trending/rss?geo=KR"
    response = requests.get(url)
    root = ET.fromstring(response.content)

    items = []
    for item in root.findall(".//item"):
        keyword = item.findtext("title")
        pub_date = item.findtext("pubDate")
        traffic = item.findtext("{https://trends.google.com/trending/rss}approx_traffic")

        items.append({
            "키워드": keyword,
            "발행일": pub_date,
            "검색량": traffic
        })

    return pd.DataFrame(items)

trends_df = get_google_trends()

st.dataframe(trends_df, use_container_width=True)
