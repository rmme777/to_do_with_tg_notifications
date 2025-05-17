from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def show_cabinet(request):
    return render(request, "cabinet/main_cabinet.html")
