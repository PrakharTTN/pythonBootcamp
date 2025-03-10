from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import Poll, Vote
import logging
from .forms import VoteForm, UploadExcelForm
import openpyxl


class PollListView(LoginRequiredMixin, ListView):
    model = Poll
    template_name = "poll_list.html"
    context_object_name = "polls"
    login_url = "/login"


class PollDetailView(DetailView):
    model = Poll
    template_name = "poll_detail.html"
    context_object_name = "poll"

    def post(self, request):
        return redirect("greeting:vote_from")


logger = logging.getLogger("user_actions")


class VoteFormView(FormView):
    template_name = "vote_form.html"
    form_class = VoteForm
    success_url = reverse_lazy("polls:poll_list")

    def form_valid(self, form):
        poll = form.cleaned_data["poll"]
        username = form.cleaned_data["user"]
        if Vote.objects.filter(poll=poll, user=username).exists():
            return HttpResponseForbidden("You have already voted for poll.")

        Vote.objects.create(poll=poll, user=username)
        logger.info(f"User  {username} voted for: {poll}")
        return super().form_valid(form)


class UploadFileView(View):

    def get(self, request):
        form = UploadExcelForm()
        return render(request, "upload_excel.html", {"form": form})

    def post(self, request):
        form = UploadExcelForm(request.POST, request.FILES)
        if form.is_valid():
            workbook = openpyxl.load_workbook(
                filename=request.FILES["file"], data_only=True
            )
            sheet = workbook.active
            data = []
            for row in sheet.iter_rows(values_only=True):
                question = row
                Poll.objects.create(question_text=question)
                data.append(row)
            return render(request, "display_data.html", {"data": data})

        return render(request, "upload_excel.html", {"form": form})


# def active_polls_view(request):
#     active_polls = Poll.objects.active()  # Use the custom manager method
#     return render(request, "active_polls.html", {"polls": active_polls})


# def recent_polls_view(request):

#     recent_polls = (
#         Poll.objects.created_within_last_week()
#     )  # Use the custom manager method
#     return render(request, "recent_polls.html", {"polls": recent_polls})


# def votes_for_poll_view(request, poll_id):
#     poll = Poll.objects.get(id=poll_id)
#     votes = Vote.objects.for_poll(poll)  # Use the custom manager method
#     return render(request, "votes_for_poll.html", {"poll": poll, "votes": votes})
