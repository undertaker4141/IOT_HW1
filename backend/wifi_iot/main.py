from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI(title="AIoT WiFi Sensor Backend")

# 資料庫路徑 (與此腳本同目錄下的 aiotdb.db)
DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aiotdb.db")

# 定義接收的資料結構 (JSON)
class SensorData(BaseModel):
    temp: float
    humid: float

def init_db():
    """初始化資料庫與資料表"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id          INTEGER  PRIMARY KEY AUTOINCREMENT,
            temp        REAL     DEFAULT 0.0,
            humid       REAL     DEFAULT 0.0,
            created_at  DATETIME DEFAULT (datetime('now', 'localtime')),
            updated_at  DATETIME DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup_event():
    # 啟動時確保資料表存在
    init_db()
    print(f"📦 Database initialized at {DB_FILE}")

@app.post("/api/sensor")
def receive_sensor_data(data: SensorData):
    """接收來自 Edge 端 (ESP32) 的溫濕度資料並存入 SQLite"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 插入資料，created_at 和 updated_at 由 SQLite 預設值處理
        cursor.execute(
            "INSERT INTO sensor_data (temp, humid) VALUES (?, ?)",
            (data.temp, data.humid)
        )
        conn.commit()
        record_id = cursor.lastrowid
        conn.close()
        
        print(f"✅ Received and Saved: ID={record_id}, Temp={data.temp}°C, Humid={data.humid}%")
        return {"status": "success", "id": record_id, "message": "Data saved"}
        
    except Exception as e:
        print(f"❌ Error saving data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sensor")
def get_sensor_data(limit: int = 10):
    """取得最近幾筆溫濕度資料 (供測試用)"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM sensor_data ORDER BY id DESC LIMIT ?", (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        results = [
            {"id": r[0], "temp": r[1], "humid": r[2], "created_at": r[3], "updated_at": r[4]}
            for r in rows
        ]
        return {"status": "success", "data": results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
