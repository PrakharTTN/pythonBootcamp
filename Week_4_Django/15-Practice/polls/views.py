from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import QuestionModel, ChoiceModel
from .forms import QuestionForm, ChoiceFormSet


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return QuestionModel.objects.order_by("pub_date")


# def index(request):
#     latest_question_list = QuestionModel.objects.order_by("-pub_date")[:5]
#     return render(
#         request,
#         "polls/index.html",
#         {"latest_question_list": latest_question_list},
#     )


class DetailsView(generic.DetailView):
    template_name = "polls/question.html"
    context_object_name = "question_details"
    model = QuestionModel


# def detail(request, question_id):
#     question_details = get_object_or_404(QuestionModel, id=question_id)
#     return render(
#         request,
#         "polls/question.html",
#         {"question_details": question_details},
#     )


class ResultsView(generic.DetailView):
    model = QuestionModel
    template_name = "polls/results.html"
    context_object_name = "question_results"


# def results(request, question_id):
#     question_results = get_object_or_404(QuestionModel, id=question_id)
#     print(question_results)
#     return render(
#         request,
#         "polls/results.html",
#         {"question_results": question_results},
#     )


class QuestionCreateView(generic.CreateView):
    form_class = QuestionForm
    model = QuestionModel
    template_name = "polls/add.html"

    def form_valid(self, form):
        question = form.save()

        choice_formset = ChoiceFormSet(self.request.POST)

        if choice_formset.is_valid():
            print("choice set is valid")
            for form in choice_formset:
                print(form)
                choice = form.save(commit=False)
                choice.question = question
                print(question)
                choice.save()
                print("saved")

        return redirect("polls:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["choice_formset"] = ChoiceFormSet(queryset=ChoiceModel.objects.none())
        return context


def vote(request, question_id):
    question = get_object_or_404(QuestionModel, id=question_id)
    if request.method == "POST":
        try:
            selected_choice = question.choice.get(pk=request.POST["choice"])
        except (KeyError, ChoiceModel.DoesNotExist):
            return render(
                request,
                "polls/votes.html",
                {"question": question, "error_message": "You didn't select a choice."},
            )

        selected_choice.votes += 1
        selected_choice.save()

        return redirect("polls:results", question_id=question.id)
    return render(request, "polls/votes.html", {"question": question})
