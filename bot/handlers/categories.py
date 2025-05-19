from aiogram import Router
from aiogram.types import Message
from utils.api import get_categories

router = Router()

@router.message(lambda msg: msg.text == "📂 Категории")
async def list_categories(message: Message):
    categories = await get_categories()
    if not categories:
        await message.answer("Категории не найдены.")
        return
    text = "📂 *Категории:*" + "\n".join([f"- {cat['name']}" for cat in categories])
    await message.answer(text, parse_mode="Markdown")
