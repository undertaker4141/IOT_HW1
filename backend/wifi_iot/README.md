# 🌐 AIoT WiFi 後端測試專案 (Backend)

> 輕量級的 FastAPI 伺服器，負責接收 ESP32 邊緣裝置透過 WiFi 發送過來的溫濕度感測資料，並將其寫入 SQLite 資料庫中。

## 📁 專案結構

```
backend/wifi_iot/
├── main.py                 # FastAPI 主程式：接收資料與寫入資料庫
├── pyproject.toml          # 專案設定檔與依賴管理
├── README.md               # 本文件
├── .python-version         # Python 版本鎖定 (3.12)
└── aiotdb.db               # (執行後自動產生) SQLite 資料庫
```

## 📋 資料庫結構 (`sensor_data`)

與先前測試相同，表結構如下：

- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `temp`: REAL DEFAULT 0.0
- `humid`: REAL DEFAULT 0.0
- `created_at`: DATETIME DEFAULT (datetime('now', 'localtime'))
- `updated_at`: DATETIME DEFAULT (datetime('now', 'localtime'))

## 🚀 環境安裝與啟動指令

請在終端機 (VSCode Terminal) **依序執行以下指令**：

### 1. 安裝系統依賴套件

由於需要接收 HTTP 請求，必須安裝 fastapi 跟 uvicorn：

```bash
cd backend/wifi_iot
uv add fastapi uvicorn
```

### 2. 啟動伺服器

使用 Uvicorn 啟動 FastAPI 伺服器，並綁定本機與所有網卡 (`0.0.0.0`) 以允許手機熱點網路中的 ESP32 存取：

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

> **⚠️ 注意事項：**
>
> 1. 當防火牆跳出提示時，**請務必允許存取**。
> 2. 請找出你電腦在此**手機熱點**網路下的 IP 地址 (可用 `ipconfig` 尋找 IPv4 位址，通常為 `192.168.43.x` 等格式)，並將此 IP 填入 ESP32 的韌體設定 (`main.cpp` 的 `serverUrl`) 中！

## 📡 API Endpoints

- **`POST /api/sensor`**
  - 用途：接收來自 ESP32 的資料
  - Payload 原型：`{"temp": 25.5, "humid": 60.0}`
- **`GET /api/sensor`**
  - 用途：透過瀏覽器快速查看最近收到的 10 筆資料 (測試用)
  - 網址：`http://127.0.0.1:8000/api/sensor`
