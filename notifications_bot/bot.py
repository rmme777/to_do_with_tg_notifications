from time import timezone
from zoneinfo import ZoneInfo

from database import (django_db_setup, save_to_db, get_from_notifbot_by_token, get_from_notifbot_by_chat_id,
                      turn_off_notification_setting, get_from_tasks_to_complete_by_user_id,
                      get_from_tasks_to_complete_by_task_id, delete_task, save_complete_to_completed)
from admin import bot_started, bot_deactivated
from aiogram import Dispatcher, Bot
from _config import TOKEN
from aiogram.filters import Command
import asyncio
import logging
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Router, F
from notifications_bot.middlewares.async_sheduler import SchedulerMiddleware, AsyncIOScheduler
import datetime
from middlewares.async_sheduler import start_send_message_scheduler

django_db_setup()
from cabinet.models import NotificationBot
from django.utils import timezone

router = Router()



async def commands(bot_: Bot):
    command = [
        BotCommand(command='start', description='Запустить бота')
    ]
    await bot_.set_my_commands(command, BotCommandScopeDefault())


@router.message(Command(commands=['start']))
async def auth(message: Message, bot: Bot, scheduler: AsyncIOScheduler):
    args = message.text.split()
    if len(args) == 2:
        uuid_token = args[1]
        try:
            notif = await get_from_notifbot_by_token(uuid_token)
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
            await start_send_message_scheduler(send_notification, message, bot, scheduler,
                                               notif.notifications_included, notif.user_id)
            await message.answer("Уведомления успешно подключены! Для настройки уведомлений перейдите на сайт.",
                                 reply_markup=reply_keyboard)
            print(f"[INFO] Пользователь {message.chat.id} успешно авторизован с токеном {uuid_token}")


        except NotificationBot.DoesNotExist:
           await message.bot.send_message(message.chat.id, "Неверная или устаревшая ссылка.")
           print(f"[WARN] Не найден токен {uuid_token} для пользователя {message.chat.id}")
    else:
        notif = await get_from_notifbot_by_chat_id(message.chat.id)

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
            await start_send_message_scheduler(send_notification, message, bot, scheduler,
                                               notif.notifications_included, notif.user_id)
            await message.answer("Вы уже авторизованы🔑 Для настройки уведомлений перейдите на сайт.", reply_markup=reply_keyboard)
        else:
            await message.answer(
                "Вы не авторизованы🚫\n"
                "Для авторизации перейдите в личный кабинет на сайте и нажмите 'Подключить уведомления'."
            )


@router.message(F.text.in_(['Уведомления включены✅', 'Уведомления отключены❌']))
async def toggle_notifications(message: Message):
    try:
        notif = await get_from_notifbot_by_chat_id(message.chat.id)
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


async def check_deadlines(message: Message):
    notif = await get_from_notifbot_by_chat_id(message.chat.id)
    tasks = await get_from_tasks_to_complete_by_user_id(notif.user_id)
    notifs_to_send = []
    for task in tasks:
        if not task.notification_time:
            continue
        if datetime.datetime.now(ZoneInfo("Europe/Kyiv")) >= task.notification_time:
            notifs_to_send.append((task.task_text, task.task_deadline - task.notification_time, task.id))
    return notifs_to_send if notifs_to_send else None


async def send_notification(message: Message, bot: Bot):
    notif = await get_from_notifbot_by_chat_id(message.chat.id)
    ck_deadlines_return = await check_deadlines(message)
    if ck_deadlines_return:
        for task_text, time_to_deadline, task_id in ck_deadlines_return:
            if notif.notifications_included:
                await bot.send_message(
                    message.chat.id,
                    text=f"Новое уведомление!\nДедлайн задачи '{task_text}' закончится через {time_to_deadline}"
                )
                task_to_delete = await get_from_tasks_to_complete_by_task_id(task_id)
                if task_to_delete:
                    await save_complete_to_completed(task_to_delete.task_text, timezone.now(), task_to_delete.user_id)
                    await delete_task(task_to_delete)


async def main():
    logging.basicConfig(
        level=logging.INFO
    )
    bot = Bot(TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    scheduler = AsyncIOScheduler(timezone='Europe/Kyiv')
    scheduler.start()
    router.message.middleware(SchedulerMiddleware(scheduler))
    router.message.register(send_notification)


    dp.startup.register(bot_started)
    dp.shutdown.register(bot_deactivated)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



