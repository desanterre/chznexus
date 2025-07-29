import asyncio
from typing import Set, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Form, Request, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from chznexus.bot.auth import ChapatizClient
from chznexus.bot.bot import connect

app = FastAPI()
templates = Jinja2Templates(directory="chznexus/templates")

class BotState:
    def __init__(self):
        self.task: Optional[asyncio.Task] = None
        self.websockets: Set[WebSocket] = set()
        self.running: bool = False

bot_state = BotState()

def get_bot_state():
    return bot_state

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/", response_class=HTMLResponse)
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    client = ChapatizClient()
    try:
        client.fetch_login_token()
        client.login(email, password)
    except Exception as e:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": f"Login failed: {str(e)}"}
        )
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie("user", email)
    return response

@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    bot: BotState = Depends(get_bot_state),
    user: Optional[str] = Cookie(default=None)
):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "bot_running": bot.running,
            "user": user,
            "error": None
        }
    )

@app.get("/bot-status")
async def bot_status(bot: BotState = Depends(get_bot_state)):
    return {"running": bot.running}

@app.post("/toggle-bot")
async def toggle_bot(bot: BotState = Depends(get_bot_state)):
    if not bot.running:
        if not bot.task or bot.task.done():
            bot.task = asyncio.create_task(run_bot(bot))
        bot.running = True
        status = "started"
    else:
        if bot.task:
            bot.task.cancel()
            try:
                await bot.task
            except asyncio.CancelledError:
                pass
        bot.running = False
        status = "stopped"
    return {"status": status}

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("user")
    return response

async def run_bot(bot: BotState):
    async def log_fn(msg: str):
        for ws in bot.websockets.copy():
            try:
                await ws.send_text(msg)
            except Exception:
                bot.websockets.discard(ws)
    await connect(log_fn=log_fn)

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket, bot: BotState = Depends(get_bot_state)):
    await ws.accept()
    bot.websockets.add(ws)
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        bot.websockets.discard(ws)
