from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Мои задачи")],
            [KeyboardButton(text="➕ Добавить задачу")],
            [KeyboardButton(text="📂 Категории")]
        ],
        resize_keyboard=True
    )
