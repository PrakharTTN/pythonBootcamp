from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from .models import Question
from django.shortcuts import get_object_or_404
from django.http import request
from .forms import QuestionForm


def add_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid:
            form.save()


def get_question(request):
    questions = Question.objects.all()
    return (request, {"Questions": questions})
