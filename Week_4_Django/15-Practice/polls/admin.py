from django.contrib import admin
from .models import QuestionModel, ChoiceModel

# Register your models here.
admin.site.register(QuestionModel)
admin.site.register(ChoiceModel)
