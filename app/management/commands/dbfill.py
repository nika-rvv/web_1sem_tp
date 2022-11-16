from random import choice
from itertools import islice
from django.core.management.base import BaseCommand
from app.models import Profile, Tag, Question, Answer, Question_Vote, Answer_Vote
from django.contrib.auth.models import User
from faker import Faker
import glob
import random
from random import shuffle, seed
from faker.providers.person.en import Provider

faker = Faker()


class Command(BaseCommand):
    def add_arguments(self, parcer):
        parcer.add_argument("-u", "--users", type=int)
        parcer.add_argument("-t", "--tags", type=int)
        parcer.add_argument("-q", "--questions", type=int)
        parcer.add_argument("-a", "--answers", type=int)
        parcer.add_argument("-qv", "--question_votes", type=int)
        parcer.add_argument("-av", "--answer_votes", type=int)
        parcer.add_argument("-all", "--all", type=int)
        parcer.add_argument("-vc", "--corr_votes")
        parcer.add_argument("-vca","--corr_votes_answers")
        

    def handle(self, *args, **options):
        users_amount = options["users"]
        questions_amount = options["questions"]
        answers_amount = options["answers"]
        tags_amount = options["tags"]
        question_votes_amount = options["question_votes"]
        answer_votes_amount = options["answer_votes"]
        total_amount = options["all"]
        correct_votes = options["corr_votes"]
        correct_votes_answers = options["corr_votes_answers"]

        if total_amount:
            self.fill_tags(total_amount * 10)
            self.fill_users(total_amount * 10)
            self.fill_questions(total_amount * 100)
            self.fill_answers(total_amount * 1000)
            self.fill_question_votes(total_amount * 2000)
            self.fill_answer_votes(total_amount * 2000)
        if tags_amount:
            self.fill_tags(tags_amount * 10)
        if users_amount:
            self.fill_users(users_amount * 10)
        if questions_amount:
            self.fill_questions(questions_amount * 100)
        if answers_amount:
            self.fill_answers(answers_amount * 1000)
        if question_votes_amount:
            self.fill_question_votes(question_votes_amount * 2000)
        if answer_votes_amount:
            self.fill_answer_votes(answer_votes_amount * 2000)
        if correct_votes:
            self.fill_correct_votes()
        if correct_votes_answers:
            self.fill_correct_votes_answers()
        

    def fill_questions(self, n):
        users = list(Profile.objects.values_list("id", flat=True))
        tags = list(Tag.objects.values_list("id", flat=True))
        for i in range(n):
            question = Question.objects.create(author_id=choice(users),
                                                title=faker.sentence()[:128],
                                                text=". ".join(faker.sentences(
                                                faker.random_int(min=2, max=5))),
                                                date=faker.date_between("-100d", "today"))
            question.tags.add(choice(tags))


    def fill_answers(self, n):
        questions = list(Question.objects.values_list("id", flat=True))
        users = list(Profile.objects.values_list("id", flat=True))
        answers = []

        for i in range(n):
            answer = Answer(question_id=choice(questions),
                            author_id=choice(users),
                            text=". ".join(faker.sentences(faker.random_int(min=2, max=5))))
            answers.append(answer)

        batch_size = 1000
        n_batches = len(answers) // batch_size
        if len(answers) % batch_size != 0:
            n_batches += 1
        for i in range(n_batches):
            start = batch_size * i
            end = batch_size * (i + 1)
            Answer.objects.bulk_create(answers[start:end], batch_size)

    def fill_users(self, n):
        usernames = set()

        file_path_type = "static/icons/*.jpg"
        images = glob.glob(file_path_type)


        while len(usernames) != n:
            usernames.add(faker.user_name() +
                          str(faker.random.randint(0, 1000000)))

        for name in usernames:
            user = User.objects.create(
                username=name, password=faker.password(), email=faker.email())
            Profile.objects.create(
                user=user, nickname=faker.name(),avatar=choice(images))
        

    def fill_tags(self, n):
        first_names = list(set(Provider.first_names))
        seed(4321)
        shuffle(first_names)

        for i in range(n):
            Tag.objects.create(tag=faker.word()+"_"+faker.word()+str(faker.random.randint(0,1000)))

    def fill_question_votes(self, n):
        questions = list(Question.objects.values_list("id", flat=True))
        users = list(Profile.objects.values_list("id", flat=True))
        votes = []

        for i in range(n):
            vote = Question_Vote(question_id=choice(questions), user_id=choice(
                users), vote=faker.random.randint(-1, 1))
            votes.append(vote)

        batch_size = 1000
        n_batches = len(votes) // batch_size
        if len(votes) % batch_size != 0:
            n_batches += 1
        for i in range(n_batches):
            start = batch_size * i
            end = batch_size * (i + 1)
            Question_Vote.objects.bulk_create(votes[start:end], batch_size)

    def fill_answer_votes(self, n):
        answers = list(Answer.objects.values_list("id", flat=True))
        users = list(Profile.objects.values_list("id", flat=True))
        votes = []

        for i in range(n):
            vote = Answer_Vote(answer_id=choice(answers), user_id=choice(
                users), vote=faker.random.randint(-1, 1))
            votes.append(vote)

        batch_size = 1000
        n_batches = len(votes) // batch_size
        if len(votes) % batch_size != 0:
            n_batches += 1
        for i in range(n_batches):
            start = batch_size * i
            end = batch_size * (i + 1)
            Answer_Vote.objects.bulk_create(votes[start:end], batch_size)
    
    def fill_correct_votes(self):
        for i in range(1,Question.objects.count()+1):
            sum = 0
            qs = Question_Vote.objects.filter(question=i)
            for j in range(qs.count()):
                sum += qs[j].vote
            result = Question.objects.get(id=i)
            result.rating = 0
            result.rating += sum
            result.save()
    
    def fill_correct_votes_answers(self):
        count = Answer.objects.count()
        for i in range(1,count+1):
            sum = 0
            qs = Answer_Vote.objects.prefetch_related('answer').filter(answer=i)
            for j in range(qs.count()):
                sum += qs[j].vote
            result = Answer.objects.get(id=i)
            result.rating = 0
            result.rating += sum
            if (i % 10000 == 0):
                print(i)
            result.save()

