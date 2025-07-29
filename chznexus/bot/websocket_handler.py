# chznexus/bot/websocket_handler.py
import asyncio
from threading import Thread

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from chznexus.bot.bot import connect
from chznexus.bot.auth import ChapatizClient

templates = Jinja2Templates(directory="chznexus/templates")

router = APIRouter()

bot_thread = None
bot_running = False
log_buffer = []
stop_event = asyncio.Event()

# Simple in-memory session storage keyed by email (for demo only)
user_sessions = {}


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, email: str = Form(...), password: str = Form(...)):
    client = ChapatizClient()
    try:
        client.fetch_login_token()
        client.login(email, password)
        user_sessions[email] = client.get_session()
    except Exception as e:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": f"Login failed: {str(e)}"}
        )
    # Redirect to your main page or dashboard after login
    return RedirectResponse(url="/", status_code=303)


def run_bot():
    async def logger(msg):
        log_buffer.append(msg)
        if len(log_buffer) > 100:
            log_buffer.pop(0)

    async def main():
        stop_event.clear()
        bot = asyncio.create_task(connect(log_fn=logger))
        try:
            await stop_event.wait()
        finally:
            bot.cancel()
            try:
                await bot
            except asyncio.CancelledError:
                log_buffer.append("🛑 Bot disconnected")

    asyncio.run(main())


@router.post("/toggle", response_class=HTMLResponse)
async def toggle():
    global bot_thread, bot_running
    if not bot_running:
        if bot_thread is None or not bot_thread.is_alive():
            bot_thread = Thread(target=run_bot, daemon=True)
            bot_thread.start()
        bot_running = True
    else:
        stop_event.set()
        bot_running = False

    return RedirectResponse(url="/", status_code=303)
