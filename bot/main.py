import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message as TgMessage
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

API_TOKEN = "7915580570:AAG-EGOkSK2tS1t_NN1eMnHdcOSFtL7Bbzg"

# Initialize Telegram bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Initialize FastAPI app
app = FastAPI()

# Include your existing routers
from handlers import start, tasks, categories

dp.include_router(start.router)
dp.include_router(tasks.router)
dp.include_router(categories.router)

# Pydantic model for incoming JSON payload
class SendMessageRequest(BaseModel):
    telegram_id: int
    text: str

@app.post("/send_message")
async def send_message_endpoint(payload: SendMessageRequest):
    """
    Send a message to a user via Telegram bot.

    - **telegram_id**: Telegram chat ID to send the message to
    - **text**: Message text
    """
    try:
        await bot.send_message(chat_id=payload.telegram_id, text=payload.text)
        return {"status": "success", "telegram_id": payload.telegram_id}
    except Exception as e:
        # If sending failed, return HTTP 500 with the error message
        raise HTTPException(status_code=500, detail=str(e))

async def start_polling_and_api():
    # Run both the Telegram polling and FastAPI server concurrently
    api_server = uvicorn.Server(
        uvicorn.Config(
            app,
            host="0.0.0.0",
            port=8001,
            log_level="info",
        )
    )
    await asyncio.gather(
        dp.start_polling(bot),
        api_server.serve(),
    )

if __name__ == "__main__":
    asyncio.run(start_polling_and_api())
