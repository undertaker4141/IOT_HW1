# 📊 AIoT 網頁控制與視覺化前端 (Frontend)

本目錄包含整個 AIoT 專題的 Web 介面。它主要由兩個獨立的元件組成：提供控制模擬器開關的原生 HTML/JS 網頁，以及即時顯示溫濕度變化曲線的 Streamlit 儀表板。

## 📁 目錄結構

```text
frontend/
├── app.py              # Streamlit 即時視覺化儀表板程式
├── index.html          # Web 控制面板：負責控制後端模擬器的啟停與最新資料查詢
└── requirements.txt    # 執行 Streamlit 儀表板所需的 Python 依賴清單
```

## ✨ 基本功能介紹

### 1. Web 控制面板 (`index.html`)
這是一個不需要安裝任何套件、直接用瀏覽器就能開啟的靜態網頁。它使用原生的 JavaScript (Fetch API) 與後端 FastAPI (`backend/wifi_iot/main.py`) 互動。

- **功能重點**：
  - **Start / Stop 按鈕**：呼叫後端的 `/api/simulator/on` 或 `/off`，讓後端開始在背景每兩秒自動產生隨機資料並寫入 SQLite 資料庫 (取代真的 ESP32 傳輸)。
  - **最新資料顯示**：網頁會定時呼叫 `/api/sensor` 拉取資料庫中最新的一筆資料，驗證連線狀況。
- **如何使用**：
  - 先確保**後端 FastAPI 伺服器**已經啟動。
  - 直接在檔案總管對 `index.html` 點兩下，或拖曳至瀏覽器中即可開啟。

### 2. 即時視覺化儀表板 (`app.py`)
使用 Streamlit 框架打造的即時圖表介面。它會直接讀取後端資料夾下的 `aiotdb.db` 資料庫檔案，並且透過無窮迴圈定時刷新畫面。

- **功能重點**：
  - **動態折線圖**：自動繪製最新幾筆溫濕度資料的曲線圖。
  - **最新指標 (Metrics)**：大字體顯示當前最新的溫度與濕度數值。
  - **筆數控制**：提供拉桿，讓您可以動態調整圖表欲顯示的資料筆數 (例如只看最新的 50 筆或 100 筆)。
- **如何使用**：
  - 開啟終端機 (Terminal) 並切換到此 `frontend` 資料夾。
  - 執行以下指令安裝依賴並啟動：
    ```bash
    pip install -r requirements.txt
    python -m streamlit run app.py
    ```
