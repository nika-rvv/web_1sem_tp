from django.db import models

# Create your models here.

Questions = [
    {
        'question_id': question_id,
        'title': f'Question #{question_id}',
        'text': f'Text of question #{question_id}'
    } for question_id in range(10)
]