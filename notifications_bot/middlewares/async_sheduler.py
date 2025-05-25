from aiogram import BaseMiddleware, Bot
from aiogram.types import Message
from typing import Callable, Awaitable, Dict, Any
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from functools import partial

from notifications_bot.database import turn_off_notification_setting


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        self.scheduler = scheduler

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        data['scheduler'] = self.scheduler
        return await handler(event, data)

async def start_send_message_scheduler(func, message: Message, bot: Bot, scheduler: AsyncIOScheduler, notif_state: bool, user_id):
    """
    function for connecting the scheduler in send_notification
    :param func: send_notification function
    :param message: Message
    :param bot: Bot
    :param scheduler:AsyncIOScheduler
    :param notif_state: notif.notifications_included
    :param user_id: notif.user_id
    """
    if notif_state:
        scheduler.add_job(
            partial(func, message, bot),
            'interval',
            seconds=5,
            id=str(message.chat.id),
            replace_existing=True
        )
    else:
        await turn_off_notification_setting(user_id)
        try:
            scheduler.remove_job(str(message.chat.id))
        except Exception:
            pass