from django.db import models
from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from datetime import date

class QuestionManager(models.Manager):
    def new(self):
        return self.select_related().order_by("-date")
    
    def popular(self):
        return self.select_related().order_by("-rating")

    def find_by_id(self, pk):
        try:
            question = self.get(id=pk)
        except ObjectDoesNotExist:
            raise Http404
        return question

    def popular_quest_by_tag(self,tag):
        return self.select_related().filter(tags=tag.id).order_by("-rating")

class AnswerManager(models.Manager):
    def popular_ans_to_question(self,pk):
        return self.select_related().filter(question=pk).order_by("-rating")

class TagManager(models.Manager):
    def find_by_tag(self, tag):
        try:
            tag = self.get(tag=tag)
        except ObjectDoesNotExist:
            raise Http404
        return tag

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='uploads/avatars/', blank=True, default="img/Component_1.jpg")
    nickname = models.CharField(max_length=255, default="Quest")

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Tag(models.Model):
    tag = models.CharField(max_length=255, unique=True, default="default_tag")

    objects = TagManager()

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    tags = models.ManyToManyField('Tag')
    rating = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    author = models.ForeignKey('Profile', on_delete=models.CASCADE)
    text = models.TextField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="answers")
    rating = models.IntegerField(default=0)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.question.title + ' ' + self.author.user.username
    
    objects = AnswerManager()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def update_score(self):
        vote_sum = self.question.all().aggregate(Sum('vote'))
        self.rating = vote_sum['vote__sum']
        self.save(update_fields=['rating'])
        return self.rating


class Question_Vote(models.Model):
    like = 1
    dislike = -1
    none = 0
    votes = [(like, 'like'), (dislike, 'dislike'), (none, 'none'), ]

    vote = models.IntegerField(choices=votes, default=none)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.question.title + ' ' + self.user.nickname + ' ' + str(self.vote)

    class Meta:
        verbose_name = 'Оценка Вопроса'
        verbose_name_plural = 'Оценки Вопросов'
    
    def update_rating(self):
            self.question.rating += self.vote


class Answer_Vote(models.Model):
    like = 1
    dislike = -1
    none = 0
    votes = [(like, 'like'), (dislike, 'dislike'), (none, 'none'), ]

    vote = models.IntegerField(choices=votes, default=none)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)

    def __str__(self):
        return self.answer.question.title + ' ' + self.user.nickname+ ' ' + str(self.vote)

    class Meta:
        verbose_name = 'Оценка Ответа'
        verbose_name_plural = 'Оценки Ответов'
