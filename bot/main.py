import asyncio
from aiogram import Bot, Dispatcher
from handlers import start, tasks, categories

API_TOKEN = "7915580570:AAG-EGOkSK2tS1t_NN1eMnHdcOSFtL7Bbzg"

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # Регистрация хендлеров
    dp.include_router(start.router)
    dp.include_router(tasks.router)
    dp.include_router(categories.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
