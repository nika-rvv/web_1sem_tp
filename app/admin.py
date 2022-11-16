from django.contrib import admin

# Register your models here.
from app.models import Profile, Tag, Question, Answer, Question_Vote, Answer_Vote

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Question_Vote)
admin.site.register(Answer_Vote)