from django.contrib import admin
from polls.models import Question, Choice
# Register your models here.


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3
class ChoiceInline2(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Add Question', {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"],"classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline2]
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

admin.site.register(Question,QuestionAdmin)
