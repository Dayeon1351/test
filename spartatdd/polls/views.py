from django.shortcuts import render
from .models import Question
from django.utils import timezone


def index(request):
    question_list = Question.objects.all().filter(
        pub_date__lte=timezone.now()
    )
    context = {'question_list': question_list}

    return render(request, 'polls/index.html', context)