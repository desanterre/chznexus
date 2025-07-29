import asyncio
import urllib.parse
from datetime import datetime

from chznexus.bin.config import CHAT_LOG_FILE

from .utils import double_url_encode


async def send_chat_message(websocket, message: str):
    encoded_msg = double_url_encode(message)
    msg_length = len(encoded_msg)
    speak_message = f"wy13:ClientMessagey5:SPEAK:2y{msg_length}:{encoded_msg}f"
    await websocket.send(speak_message)
    print(f"📨 Sent message: {message}")


async def terminal_input_loop(websocket):
    loop = asyncio.get_event_loop()
    while True:
        message = await loop.run_in_executor(
            None, input, "📝 Enter message (/quit to stop): "
        )
        if message.strip().lower() == "/quit":
            print("👋 Exiting terminal input loop.")
            break
        await send_chat_message(websocket, message)


def handle_user_talk(message, user_map):
    import re
    import urllib.parse
    from datetime import datetime

    match = re.search(r"5i(\d+)y(\d+):", message)
    if match:
        user_id = match.group(1)
        message_text_encoded = message.split(f"5i{user_id}y{match.group(2)}:")[1].split(
            "y"
        )[0]
        decoded_text = urllib.parse.unquote(urllib.parse.unquote(message_text_encoded))
        username = user_map.get(user_id, "Unknown")
        log_line = f"[{datetime.now().strftime('%H:%M:%S')}] User {username} ({user_id}): {decoded_text}"
        print("💬", log_line)
        with open(CHAT_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
        return log_line
    return None
