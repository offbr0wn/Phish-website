from django.contrib import admin

from .forms import ChoiceForm, ChoiceInlineFormset, QuestionForm
from .models import Question, Choice, Question1, Choice1





class ChoiceInline(admin.TabularInline):
    model = Choice
    can_delete = True
    max_num = Choice.MAX_CHOICES_COUNT
    min_num = Choice.MAX_CHOICES_COUNT
    form = ChoiceForm
    formset = ChoiceInlineFormset


class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = (ChoiceInline,)
    list_display = ['html']

    search_fields = ['html', 'choices__html']
    actions = None
    form = QuestionForm


class ChoiceInline1(admin.TabularInline):
    model = Choice1
    can_delete = True
    max_num = Choice1.MAX_CHOICES_COUNT
    min_num = Choice1.MAX_CHOICES_COUNT
    form = ChoiceForm
    formset = ChoiceInlineFormset


class QuestionAdmin1(admin.ModelAdmin):
    model = Question1
    inlines = (ChoiceInline1,)
    exclude = [ 'is_published', 'maximum_marks']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Question1, QuestionAdmin1)

