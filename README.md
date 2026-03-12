# 🌐 AIoT 溫濕度感測與 WiFi 串接專題 (ESP32)

本專案是一個完整的物聯網 (IoT) 實作測試，涵蓋了邊緣裝置 (Edge) 的硬體控制、感測器讀取，以及後端 (Backend) 的 API 接收與資料庫儲存。

整個專案架構分為 `edge/` (ESP32 硬體端) 與 `backend/` (伺服器端) 兩大部分。

---

## 📂 專案總體結構

```
d:\IOT_HW1\
├── .agent/              # AI 代理人 Skill 設定區 (task_logger)
├── backend/             # 後端伺服器與資料庫測試區 (Python / uv)
│   ├── mock_db/         # 產生模擬 SQLite 測試資料的專案
│   └── wifi_iot/        # 接收 ESP32 上傳真實數據的 FastAPI 伺服器
├── edge/                # 邊緣運算硬體專案區 (C++ / PlatformIO)
│   ├── DHT11/           # 【測試一】單純讀取 DHT11 溫濕度並印在 Serial
│   ├── DHT11_WIFI/      # 【正式串接】讀取 DHT11 溫濕度並透過 WiFi POST 到後端
│   └── LED/             # 【基礎測試】ESP32 內建 LED 閃爍測試
├── 任務紀錄.md            # AI 執行每次指令的自動紀錄檔
└── README.md            # 本專案總體說明文件 (你正在閱讀的文件)
```

---

## 🖥️ 後端專案 (Backend)

後端使用現代化的 Python 工具 `uv` 建立虛擬環境與管理依賴。

### 1. `backend/mock_db` (模擬資料庫測試)

- **用途**：在真實硬體串接前，確認 SQLite 資料庫的 Schema 與基本寫入功能。
- **技術棧**：Python 3.12 內建 `sqlite3`
- **核心檔案**：`generate_mock_data.py`
- **功能**：自動建立 `aiotdb.db` 並產生 50 筆模擬的 DHT11 溫濕度數據，支援時間戳記。

### 2. `backend/wifi_iot` (正式 API 伺服器)

- **用途**：作為真實的後端伺服器，接收來自 ESP32 的 HTTP POST 請求。
- **技術棧**：Python 3.12, `FastAPI`, `Uvicorn`, `sqlite3`
- **核心檔案**：`main.py`
- **功能**：
  - 提供 `/api/sensor` (POST) Endpoint，接收 JSON 格式的溫濕度數據。
  - 將數據寫入同目錄下的 `aiotdb.db` 資料庫 (`sensor_data` 表)。
  - 提供 `/api/sensor` (GET) Endpoint 供瀏覽器快速預覽近期數據。

---

## 📡 邊緣端專案 (Edge)

硬體端使用 VS Code 的 **PlatformIO** 擴充套件進行開發，目標板為 **ESP32 WROOM-32 (`denky32`)**。

### 1. `edge/LED` (GPIO 基礎測試)

- **用途**：驗證 ESP32 開發板與 PlatformIO 環境是否正常運作。
- **功能**：控制 GPIO 2 內建 LED 每 500ms 閃爍一次，並透過 Serial 監視器 (115200) 輸出狀態。

### 2. `edge/DHT11` (感測器讀取測試)

- **用途**：驗證 DHT11 溫濕度感測器的接線與庫函數是否正常。
- **依賴庫**：`adafruit/DHT sensor library`
- **功能**：透過 GPIO 15 定期讀取 DHT11 的溫度、濕度、體感溫度，並顯示於 Serial 監視器。具備自動錯誤偵測。

### 3. `edge/DHT11_WIFI` (軟硬體串接整合)

- **用途**：**本專題的最終整合**。將讀取到的物理數據傳送至網路上的自建伺服器。
- **依賴庫**：`WiFi.h`, `HTTPClient.h`, `adafruit/DHT sensor library`
- **功能**：
  - 連接使用者指定的手機 WiFi 熱點。
  - 每 5 秒讀取一次 DHT11 溫濕度 (GPIO 15)。
  - 將數據包裝成 JSON 格式 (`{"temp": 25.0, "humid": 50.0}`)。
  - 透過 HTTP POST 發送給位於同一個 WiFi 網域下的 FastAPI 電腦伺服器。

---

## 🚀 系統整合執行流程

要完整重現從硬體到資料庫的資料流，請依下列步驟進行：

1. **開啟手機 WiFi 熱點**，讓你的電腦與 ESP32 皆準備連接此熱點。
2. **找出電腦 IP**：在電腦開啟終端機，執行 `ipconfig`，記下 IPv4 位址 (例如 `192.168.43.x`)。
3. **啟動後端伺服器**：
   ```bash
   cd d:\IOT_HW1\backend\wifi_iot
   uv sync
   uv run uvicorn main:app --host 0.0.0.0 --port 8000
   ```
4. **設定並燒錄 ESP32 韌體**：
   - 開啟 `edge/DHT11_WIFI/src/main.cpp`
   - 修改 `ssid` 為手機熱點名稱、`password` 為熱點密碼。
   - 修改 `serverUrl` 為步驟 2 拿到的 IP (如 `"http://192.168.43.x:8000/api/sensor"`)。
   - 使用 PlatformIO 進行 **Build & Upload**。
5. **觀察結果**：
   - ESP32 連上線後，後端的終端機與 ESP32 的 Serial Monitor 皆會同步顯示送出與接收成功的數據紀錄。

---

_詳細的使用與環境設定，請參考各別目錄下的 `README.md` 指南。_
