from django.contrib import admin
from .models import QuestionModel, ChoiceModel


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]


admin.site.register(QuestionModel, QuestionAdmin)

admin.site.register(ChoiceModel)
