from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from keyboards.task_actions import task_actions_kb
from utils.api import get_tasks, create_task, get_categories
from datetime import datetime
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Список и управление существующими задачами
@router.message(lambda msg: msg.text == "📋 Мои задачи")
async def list_tasks(message: Message, state: FSMContext):
    tasks = await get_tasks(message.from_user.id)
    if not tasks:
        await message.answer("У тебя нет задач.")
        return

    # Сохраняем список в хранилище FSMContext
    await state.update_data(tasks=tasks)

    for idx, task in enumerate(tasks):
        text = (
            f"📌 *{task['title']}*\n"
            f"🗓 До: {task['due_date']}\n"
            f"📝 {task['description'] or '—'}"
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Редактировать",
                    callback_data=f"task_edit:{idx}"
                ),
                InlineKeyboardButton(
                    text="🗑 Удалить",
                    callback_data=f"task_delete:{idx}"
                ),
            ]
        ])
        await message.answer(text, reply_markup=kb, parse_mode="Markdown")

# FSM-состояния для создания задачи
class TaskCreation(StatesGroup):
    title = State()
    description = State()
    due_date = State()
    categories = State()
    category_idx = State()

# Запуск создания задачи
@router.message(lambda msg: msg.text == "➕ Добавить задачу")
async def cmd_add_task(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите заголовок задачи:")
    await state.set_state(TaskCreation.title)

# Ввод заголовка
@router.message(TaskCreation.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите описание задачи (или просто отправьте пустое сообщение):")
    await state.set_state(TaskCreation.description)

# Ввод описания
@router.message(TaskCreation.description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(
        "Введите срок исполнения в формате `YYYY-MM-DD HH:MM` (например, 2025-05-25 17:36):",
        parse_mode="Markdown"
    )
    await state.set_state(TaskCreation.due_date)

# Ввод срока исполнения
@router.message(TaskCreation.due_date)
async def process_due_date(message: Message, state: FSMContext):
    text = message.text
    try:
        due = datetime.strptime(text, "%Y-%m-%d %H:%M")
    except ValueError:
        await message.answer(
            "Неверный формат. Попробуйте ещё раз, формат должен быть `YYYY-MM-DD HH:MM`."
        )
        return
    await state.update_data(due_date=due.isoformat())

    cats = await get_categories()
    if not cats:
        await message.answer("Категории не найдены. Создайте сначала категорию.")
        await state.clear()
        return

    # Сохраняем список категорий в состоянии
    await state.update_data(categories=cats)

    # Строим inline-клавиатуру, используя индекс
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=cat["name"],
                    callback_data=f"catidx:{idx}"
                )
            ]
            for idx, cat in enumerate(cats)
        ]
    )
    await message.answer("Выберите категорию задачи:", reply_markup=keyboard)
    await state.set_state(TaskCreation.category_idx)

# Выбор категории и финализация
@router.callback_query(F.data.startswith("catidx:"), TaskCreation.category_idx)
async def process_category(call: CallbackQuery, state: FSMContext):
    idx = int(call.data.split(":", 1)[1])
    data = await state.get_data()
    cats = data.get("categories", [])
    if idx < 0 or idx >= len(cats):
        await call.answer("Неверный выбор категории.", show_alert=True)
        return

    cat_id = cats[idx]["id"]
    payload = {
        "title": data["title"],
        "description": data.get("description", ""),
        "due_date": data["due_date"],
        "category": cat_id,
        "telegram_user_id": call.from_user.id
    }
    task = await create_task(payload)
    await call.message.answer(
        f"✅ Задача *{task['title']}* создана!\n"
        f"ID: `{task['id']}`\n"
        f"До: {task['due_date']}",
        parse_mode="Markdown"
    )
    await state.clear()

# Заготовки для редактирования и удаления
@router.callback_query(F.data.startswith("edit:"))
async def edit_task(call: CallbackQuery):
    task_id = call.data.split(":", 1)[1]
    await call.message.answer(f"Здесь будет логика редактирования задачи {task_id}")

@router.callback_query(F.data.startswith("delete:"))
async def delete_task(call: CallbackQuery):
    task_id = call.data.split(":", 1)[1]
    # TODO: запрос DELETE к API
    await call.message.answer(f"Задача {task_id} удалена (имитация).")
