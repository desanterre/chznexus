# chznexus/bot/websocket_handler.py
import asyncio
from threading import Thread

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from chznexus.bot.bot import connect  # Import connect here

app = FastAPI()

bot_task = None
bot_running = False
log_buffer = []
stop_event = asyncio.Event()


def run_bot():
    async def logger(msg):
        log_buffer.append(msg)
        if len(log_buffer) > 100:
            log_buffer.pop(0)

    async def main():
        stop_event.clear()
        bot = asyncio.create_task(connect(log_fn=logger))
        await stop_event.wait()
        bot.cancel()
        try:
            await bot
        except asyncio.CancelledError:
            log_buffer.append("🛑 Bot disconnected")

    asyncio.run(main())


@app.get("/", response_class=HTMLResponse)
async def index():
    logs = "<br>".join(log_buffer)
    button_label = "Disconnect" if bot_running else "Connect"
    return f"""
        <html>
            <head><title>CHZ Nexus Bot</title></head>
            <body>
                <h1>CHZ Nexus Control Panel</h1>
                <form action="/toggle" method="post">
                    <button type="submit">{button_label}</button>
                </form>
                <h2>Logs:</h2>
                <div style="font-family: monospace; white-space: pre-wrap; border: 1px solid #ccc; padding: 1em;">{logs}</div>
            </body>
        </html>
    """


@app.post("/toggle")
async def toggle():
    global bot_task, bot_running
    if not bot_running:
        if bot_task is None or not bot_task.is_alive():
            bot_task = Thread(target=run_bot)
            bot_task.start()
        bot_running = True
    else:
        stop_event.set()
        bot_running = False
    return RedirectResponse(url="/", status_code=303)
