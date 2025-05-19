import aiohttp

BASE_URL = "http://localhost:8000/api"

async def get_tasks(telegram_user_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/tasks/", params={"telegram_user_id": telegram_user_id}) as resp:
            return await resp.json()

async def create_task(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/tasks/", json=data) as resp:
            return await resp.json()

async def get_categories():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/categories/") as resp:
            return await resp.json()

async def patch_task(task_id: str, data: dict):
    async with aiohttp.ClientSession() as session:
        async with session.patch(f"{BASE_URL}/tasks/{task_id}/", json=data) as resp:
            return await resp.json()