import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

EXCEL_FILENAME = os.path.join(DATA_DIR, "user_logins.xlsx")
CHAT_LOG_FILE = os.path.join(DATA_DIR, "user_talk_log.txt")

WS_URI = "wss://chat2.chapatiz.com/"
HEADERS = {
    "Origin": "https://www.chapatiz.com",
    "Cache-Control": "no-cache",
    "Accept-Language": "en-US,en;q=0.9",
    "Pragma": "no-cache",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N)",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
}
