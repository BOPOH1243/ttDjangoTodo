from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def task_actions_kb(task_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit:{task_id}")],
        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete:{task_id}")]
    ])
