from django.shortcuts import render
from django.http import HttpResponse
from . import models


def index(request):
    context = {'questions': models.Questions}
    return render(request, 'index.html', context=context)

def question(request, question_id: int):
    question_item = models.Questions[question_id]
    context = {'question': question_item}
    return render(request, 'question.html', context=context)

def ask(request):
    return render(request,'ask.html')

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'signup.html')

def settings(request):
    return render(request,'settings.html')