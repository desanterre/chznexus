import asyncio

from chznexus.bot.websocket_handler import connect

if __name__ == "__main__":
    asyncio.run(connect())
