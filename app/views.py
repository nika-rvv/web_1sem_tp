from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from app.models import Question, Answer, Question_Vote, Answer_Vote, Profile, Tag



def paginate(objects_list, request, per_page):
    paginator = Paginator(objects_list,per_page)
    page = request.GET.get('page')
    object_list_page = paginator.get_page(page)
    return object_list_page

def index(request):
    questions = Question.objects.new()
    questions_page = paginate(questions,request,4)
    return render(request,'index.html',{'questions':questions_page})

def ask(request):
    return render(request,'ask.html',{})

def question(request):
    return render(request,'question.html',{})

def hot(request):
    questions = Question.objects.popular()
    questions_page = paginate(questions,request,4)
    return render(request,'hot.html',{'questions': questions_page})

def one_question(request,pk):
    question = Question.objects.find_by_id(pk)
    answers = Answer.objects.popular_ans_to_question(pk)
    count = answers.count()
    answers_page = paginate(answers,request,3)
    return render(request,'question.html',{"question": question,"answers":answers_page,"count":count})

def login(request):
    return render(request,'login.html',{})

def register(request):
    return render(request,'signup.html',{})

def tag(request,tag):
    needed_tag = Tag.objects.find_by_tag(tag)
    questions = Question.objects.popular_quest_by_tag(needed_tag)
    questions_page = paginate(questions,request,4)
    return render(request,'tag.html',{'questions': questions_page,'needed_tag':needed_tag})

def settings(request):
    return render(request,'settings.html',{})
