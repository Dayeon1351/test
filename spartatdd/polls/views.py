from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from .models import Question


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id, pub_date__lte=timezone.now())
    return render(request, 'polls/detail.html', {'question': question})

def index(request):
    question_list = Question.objects.all().filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
    context = {'question_list': question_list}

    return render(request, 'polls/index.html', context)