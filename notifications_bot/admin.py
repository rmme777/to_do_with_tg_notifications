from _config import ADMIN_ID
from aiogram import Bot


async def bot_started(bot: Bot):
    await bot.send_message(ADMIN_ID, text='Бот запущен')

async def bot_deactivated(bot: Bot):
    await bot.send_message(ADMIN_ID, text='Бот отключен')