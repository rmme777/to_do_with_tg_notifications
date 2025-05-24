from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,
                               keyboard=[
                               [
                                       KeyboardButton(text='Настройка уведомлений⚙️'),
                                       KeyboardButton(text='Уведомления'),
                               ]
                                   ])

