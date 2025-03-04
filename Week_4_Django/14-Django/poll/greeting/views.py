from django.views.generic import ListView
from .models import Question
from .forms import QuestionForm


class QuestionsListView(ListView):
    pass


def add_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid:
            form.save()


def get_question(request):
    questions = Question.objects.all()
    return (request, {"Questions": questions})
