from django.shortcuts import render, redirect
from .forms import AuntieficationForm
from .models import Users




def user_register(request):
    return render(request, 'registration/register.html')
