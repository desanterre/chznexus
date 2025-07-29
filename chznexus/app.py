import asyncio
from typing import Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

bot_task = None
websockets: Set[WebSocket] = set()
bot_running = False  # track bot state


@app.get("/", response_class=HTMLResponse)
async def get():
    # Button label depends on bot_running
    button_label = "Disconnect" if bot_running else "Connect"

    return f"""
    <html>
        <head><title>ChzNexus Bot Console</title></head>
        <body>
            <h1>CHZ Nexus Bot</h1>
            <button id="toggleBtn" onclick="toggleBot()">{button_label}</button>
            <pre id="log" style="background:#111;color:#0f0;padding:1em;height:300px;overflow:auto;"></pre>
            <script>
                let ws;
                function connectWS() {{
                    ws = new WebSocket(`ws://${{location.host}}/ws`);
                    const log = document.getElementById('log');
                    ws.onmessage = event => {{
                        log.textContent += event.data + '\\n';
                        log.scrollTop = log.scrollHeight;
                    }};
                    ws.onclose = () => log.textContent += "\\n[Connection closed]";
                }}

                async function toggleBot() {{
                    const resp = await fetch('/toggle-bot', {{ method: 'POST' }});
                    const data = await resp.json();

                    document.getElementById('toggleBtn').textContent = data.status === 'started' ? 'Disconnect' : 'Connect';

                    if(data.status === 'started') {{
                        connectWS();
                    }} else {{
                        if(ws) ws.close();
                    }}
                }}

                // Connect WebSocket if bot already running on page load
                window.onload = async () => {{
                    const resp = await fetch('/bot-status');
                    const data = await resp.json();
                    if(data.running) {{
                        document.getElementById('toggleBtn').textContent = 'Disconnect';
                        connectWS();
                    }}
                }};
            </script>
        </body>
    </html>
    """


@app.get("/bot-status")
async def bot_status():
    global bot_running
    return {"running": bot_running}


@app.post("/toggle-bot")
async def toggle_bot():
    global bot_task, bot_running

    if not bot_running:
        if not bot_task or bot_task.done():
            bot_task = asyncio.create_task(run_bot())
        bot_running = True
        status = "started"
    else:
        # cancel the bot task
        if bot_task:
            bot_task.cancel()
            try:
                await bot_task
            except asyncio.CancelledError:
                pass
        bot_running = False
        status = "stopped"

    return {"status": status}


async def run_bot():
    async def mock_print(msg):
        for ws in websockets.copy():
            try:
                await ws.send_text(msg)
            except Exception:
                websockets.discard(ws)

    from chznexus.bot.bot import connect

    await connect(log_fn=mock_print)


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    websockets.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        websockets.remove(ws)
