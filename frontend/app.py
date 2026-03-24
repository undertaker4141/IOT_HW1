import streamlit as st
import sqlite3
import pandas as pd
import os
import time
import requests

# 設定網頁標題與排版
st.set_page_config(page_title="AIoT Sensor Dashboard", layout="wide")
st.title("即時溫濕度監測儀表板 🌡️💧")

# 資料庫路徑 (指向 backend/wifi_iot/aiotdb.db)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'backend', 'wifi_iot', 'aiotdb.db')
API_BASE = "http://127.0.0.1:8000/api"

# 側邊欄：模擬器控制
st.sidebar.header("🕹️ 模擬器控制面板")
if st.sidebar.button("▶️ 啟動模擬器 (Start)"):
    try:
        res = requests.post(f"{API_BASE}/simulator/on")
        if res.status_code == 200:
            st.sidebar.success("✅ 模擬器已啟動！")
    except Exception as e:
        st.sidebar.error(f"❌ 無法連線至後端API ({e})")

if st.sidebar.button("⏹️ 停止模擬器 (Stop)"):
    try:
        res = requests.post(f"{API_BASE}/simulator/off")
        if res.status_code == 200:
            st.sidebar.warning("🛑 模擬器已停止！")
    except Exception as e:
        st.sidebar.error(f"❌ 無法連線至後端API ({e})")

def fetch_data(limit=100):
    try:
        conn = sqlite3.connect(DB_PATH)
        query = f"SELECT id, temp, humid, created_at FROM sensor_data ORDER BY id DESC LIMIT {limit}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['created_at'] = pd.to_datetime(df['created_at'])
            df = df.sort_values('id') # 確保時間軸是由舊到新排列
            df.set_index('created_at', inplace=True)
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ 無法讀取資料庫: {e}")
        return pd.DataFrame()

# 使用者可以自訂顯示筆數
data_limit = st.slider("顯示最近幾筆資料", min_value=10, max_value=500, value=50, step=10)

# placeholder for dynamic update
metrics_col1, metrics_col2 = st.columns(2)
chart_placeholder = st.empty()

# 無窮迴圈來動態更新 (Streaming)
while True:
    df = fetch_data(limit=data_limit)
    
    if not df.empty:
        latest = df.iloc[-1]
        
        # 顯示最新指標
        metrics_col1.metric("最新溫度 (°C)", f"{latest['temp']} °C")
        metrics_col2.metric("最新濕度 (%)", f"{latest['humid']} %")
        
        # 顯示圖表
        chart_df = df[['temp', 'humid']]
        chart_placeholder.line_chart(chart_df)
    else:
        st.warning("⚠️ 目前資料庫中沒有任何資料")
    
    # 每 2 秒刷新一次畫面
    time.sleep(2)
    st.rerun()
