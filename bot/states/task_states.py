from aiogram.fsm.state import StatesGroup, State

class TaskCreation(StatesGroup):
    title = State()
    description = State()
    due_date = State()
    category = State()
