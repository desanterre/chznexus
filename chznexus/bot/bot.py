# chznexus/bot/bot.py
import asyncio
import re

import websockets

from chznexus.bin.config import HEADERS, WS_URI

from .chat import handle_user_talk, send_chat_message, terminal_input_loop
from .user import append_to_excel, update_user_map, user_map
from .utils import parse_login_ok, spoof_login_ok_response


async def send_ping(websocket, log_fn):
    while True:
        await asyncio.sleep(5)
        await websocket.send("wy13:ClientMessagey4:PING:0")


async def connect(log_fn=print):
    async with websockets.connect(WS_URI, additional_headers=HEADERS) as websocket:
        await log_fn("✅ Connected to WebSocket.")

        # LOGIN
        await websocket.send("wy13:ClientMessagey5:LOGIN:3y8:visiteury1:0f")
        await log_fn("📨 Sent LOGIN")

        while True:
            message = await websocket.recv()

            if "LOGIN_OK" in message:
                message = spoof_login_ok_response(message)
                await log_fn("✅ LOGIN_OK received.")

                username = parse_login_ok(message)
                user_id = message.split(":")[2]
                if username:
                    update_user_map(user_id, username)
                    append_to_excel(user_id, username)
                    await log_fn(f"👤 Logged in: {username} ({user_id})")
                break

        await websocket.send("wy13:ClientMessagey11:SET_NOQUERY:1f")
        await websocket.send("wy13:ClientMessagey11:CHANGE_ROOM:2y13:central.placen")
        await asyncio.sleep(1)
        await websocket.send("wy13:ClientMessagey5:READY:0")
        await asyncio.sleep(2)
        await send_chat_message(websocket, "Hello from spoofed visitor!")
        await log_fn("💬 Sent greeting message")

        asyncio.create_task(send_ping(websocket, log_fn))
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
                        await log_fn(f"👋 {username} ({user_id}) joined")

                elif "USER_TALK" in message:
                    clean_log = handle_user_talk(message, user_map)
                    if clean_log:
                        await log_fn(f"🗣️  {clean_log}")

                elif "USER_LEFT" in message:
                    match = re.search(r"midi(\d+)", message)
                    if match:
                        user_id = match.group(1)
                        username = user_map.get(user_id, "Unknown")
                        await log_fn(f"👋 {username} ({user_id}) left")
                        user_map.pop(user_id, None)

            except websockets.exceptions.ConnectionClosed as e:
                await log_fn(f"🔌 Connection closed: {e}")
                break
