from django.urls import path
from .views import PollListView, PollDetailView, VoteFormView

app_name = "polls"

urlpatterns = [
    path("", PollListView.as_view(), name="poll_list"),
    path("poll/<int:pk>/", PollDetailView.as_view(), name="poll_detail"),
    path("poll/<int:poll_id>/vote/", VoteFormView.as_view(), name="vote_form"),
]
