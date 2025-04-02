from django.contrib import admin
from .models import QuestionModel, ChoiceModel


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date Info", {"fields": ["pub_date"]}),
    ]

    #    fields = ["pub_date", "question_text"]


admin.site.register(QuestionModel, QuestionAdmin)

admin.site.register(ChoiceModel)
