# 📡 ESP32 DHT11 WiFi 傳送測試 (Edge 端)

> 透過手機熱點將 ESP32 連上網路，並讀取 DHT11 (GPIO 15) 的溫濕度數據，每隔 5 秒發送 HTTP POST 請求至你電腦運行的後端伺服器。

## 📁 專案結構

```
edge/DHT11_WIFI/
├── src/main.cpp            # 主程式：連接 WiFi、讀取 DHT11、發送 HTTP POST
├── platformio.ini          # PlatformIO 設定 (含 DHT 依賴庫)
└── README.md               # 本文件
```

## 🛠️ 開發前準備 (極度重要！)

在編譯與燒錄韌體之前，你**必須**先修改 `src/main.cpp` 頂部的三個設定值：

1. **`ssid`**: 你的手機熱點名稱 (WiFi Name)
2. **`password`**: 你的手機熱點密碼
3. **`serverUrl`**: 你電腦後端伺服器的 IP 地址與 API 路徑
   - 手機開啟熱點，讓電腦與 ESP32 連上**同一個熱點**。
   - 在電腦終端機輸入 `ipconfig`，找到該網路的 `IPv4 位址`。
   - 假設拿到 `192.168.43.100`，則將連結改為：`"http://192.168.43.100:8000/api/sensor"`。

## 🚀 測試步驟

1. **啟動後端**
   - 先依照 `backend/wifi_iot/README.md` 的指示啟動 fastapi 伺服器。
2. **修改與燒錄韌體**
   - 確認 `main.cpp` 的 SSID、密碼與 IP 都填寫無誤。
   - 在 PlatformIO 點擊 **"Upload"** 燒錄至 ESP32。
3. **觀察輸出**
   - 開啟 PlatformIO **Serial Monitor** (115200 baud) 觀察連接狀況與發送日誌。
   - 觀察後端終端機是否印出 `✅ Received and Saved...`，代表串接成功！
