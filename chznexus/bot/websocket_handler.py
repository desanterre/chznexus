import asyncio
import re

import websockets

from chznexus.bin.config import HEADERS, WS_URI

from .chat import handle_user_talk, send_chat_message, terminal_input_loop
from .user import append_to_excel, update_user_map, user_map
from .utils import parse_login_ok, spoof_login_ok_response


async def send_ping(websocket):
    while True:
        await asyncio.sleep(5)
        await websocket.send("wy13:ClientMessagey4:PING:0")


async def connect():
    async with websockets.connect(WS_URI, additional_headers=HEADERS) as websocket:
        print("✅ Connected to WebSocket.")

        # LOGIN
        await websocket.send("wy13:ClientMessagey5:LOGIN:3y8:visiteury1:0f")
        print("📨 Sent LOGIN")

        while True:
            message = await websocket.recv()

            if "LOGIN_OK" in message:
                message = spoof_login_ok_response(message)
                print("✅ LOGIN_OK received.")

                username = parse_login_ok(message)
                user_id = message.split(":")[2]
                if username:
                    update_user_map(user_id, username)
                    append_to_excel(user_id, username)
                break

        await websocket.send("wy13:ClientMessagey11:SET_NOQUERY:1f")
        await websocket.send("wy13:ClientMessagey11:CHANGE_ROOM:2y13:central.placen")
        await asyncio.sleep(1)
        await websocket.send("wy13:ClientMessagey5:READY:0")
        await asyncio.sleep(2)
        await send_chat_message(websocket, "Hello from spoofed visitor!")

        asyncio.create_task(send_ping(websocket))
        asyncio.create_task(terminal_input_loop(websocket))

        while True:
            try:
                message = await websocket.recv()

                if "USER_JOINED" in message:
                    match = re.search(r"midi(\d+)y4:nicky\d+:(\w+)", message)
                    if match:
                        user_id, username = match.group(1), match.group(2)
                        update_user_map(user_id, username)
                        append_to_excel(user_id, username)

                elif "USER_TALK" in message:
                    handle_user_talk(message, user_map)

                elif "USER_LEFT" in message:
                    match = re.search(r"midi(\d+)", message)
                    if match:
                        user_id = match.group(1)
                        username = user_map.get(user_id, "Unknown")
                        print(f"📤 User {username} ({user_id}) logged out.")
                        user_map.pop(user_id, None)

            except websockets.exceptions.ConnectionClosed as e:
                print("🔌 Connection closed:", e)
                break
