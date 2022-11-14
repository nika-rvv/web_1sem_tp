from django.db import models

# Create your models here.

Questions = [
    {
         'id': question_id,
         'title': f'Question #{question_id}',
         'text': f'Text of question #{question_id}',
         'answers_number': question_id * question_id,
         'tags': ['tag' for i in range(4)],
     } for question_id in range(100)
]