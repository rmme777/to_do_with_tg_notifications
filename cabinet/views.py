from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import NotificationBot
from uuid import uuid4

@login_required()
def show_cabinet(request):
    return render(request, "cabinet/main_cabinet.html")

def bot_redirect_by_token(request):
    bot, _ = NotificationBot.objects.get_or_create(user=request.user)
    bot.auth_token = uuid4()  # перегенерация токена при каждом нажатии
    bot.save()

    bot_link = f"https://t.me/todo_tgnotifications_bot?start={bot.auth_token}"
    return redirect(bot_link)


# TODO: добавить в кабинет кнопку смены пароля. В поле логина в аппке registration добавить возможность сброса пароля(email сервер)