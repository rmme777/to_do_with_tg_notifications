from database import django_db_setup, save_to_db, get_from_db_by_token, get_from_db_by_chat_id
from admin import bot_started, bot_deactivated
from aiogram import Dispatcher, Bot
from _config import TOKEN
from aiogram.filters import Command
import asyncio
import logging
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router, F

django_db_setup()
from cabinet.models import NotificationBot

router = Router()



async def commands(bot_: Bot):
    command = [
        BotCommand(command='start', description='Запустить бота')
    ]
    await bot_.set_my_commands(command, BotCommandScopeDefault())


@router.message(Command(commands=['start']))
async def auth(message: Message):
    args = message.text.split()
    if len(args) == 2:
        uuid_token = args[1]
        try:
            notif = await get_from_db_by_token(uuid_token)
            notif.telegram_chat_id = message.chat.id
            notif.authorized = True
            notif.notifications_included = True
            await save_to_db(notif)

            notif_text = 'Уведомления включены✅'
            reply_keyboard = ReplyKeyboardMarkup(
                resize_keyboard=True,
                keyboard=[                        [
                        KeyboardButton(text=notif_text)
                    ],
                ]
            )
            await message.answer("Уведомления успешно подключены! Для настройки уведомлений перейдите на сайт.",
                                 reply_markup=reply_keyboard)
            print(f"[INFO] Пользователь {message.chat.id} успешно авторизован с токеном {uuid_token}")


        except NotificationBot.DoesNotExist:
           await message.bot.send_message(message.chat.id, "Неверная или устаревшая ссылка.")
           print(f"[WARN] Не найден токен {uuid_token} для пользователя {message.chat.id}")
    else:
        notif = await get_from_db_by_chat_id(message.chat.id)

        if notif and notif.authorized:
            notif_text = 'Уведомления включены✅' if notif.notifications_included else 'Уведомления отключены❌'
            reply_keyboard = ReplyKeyboardMarkup(
                resize_keyboard=True,
                keyboard=[
                    [
                        KeyboardButton(text=notif_text)
                    ],
                ]
            )
            await message.answer("Вы уже авторизованы🔑 Для настройки уведомлений перейдите на сайт.", reply_markup=reply_keyboard)
        else:
            await message.answer(
                "Вы не авторизованы🚫\n"
                "Для авторизации перейдите в личный кабинет на сайте и нажмите 'Подключить уведомления'."
            )


@router.message(F.text.in_(['Уведомления включены✅', 'Уведомления отключены❌']))
async def toggle_notifications(message: Message):
    try:
        notif = await get_from_db_by_chat_id(message.chat.id)
        if not notif:
            await message.answer("Вы не авторизованы.")
            return

        notif.notifications_included = not notif.notifications_included
        await save_to_db(notif)

        notif_text = 'Уведомления включены✅' if notif.notifications_included else 'Уведомления отключены❌'

        reply_keyboard = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton(text=notif_text)
                ],
            ]
        )

        await message.answer(
            f"Уведомления {'включены' if notif.notifications_included else 'отключены'}",
            reply_markup=reply_keyboard
        )

    except Exception as e:
        print(f"[ERROR] toggle_notifications: {e}")
        await message.answer("Произошла ошибка.")





async def main():
    logging.basicConfig(
        level=logging.INFO
    )
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    dp.startup.register(bot_started)
    dp.shutdown.register(bot_deactivated)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



