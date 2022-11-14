from django.shortcuts import render
from django.http import HttpResponse
from . import models


def index(request):
    context = {'questions': models.Questions}
    return render(request, 'index.html', context=context)

def question(request, question_id: int):
    return render(request, 'question.html')

def ask(request):
    return render(request,'ask.html')

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'signup.html')

def settings(request):
    return render(request,'settings.html')