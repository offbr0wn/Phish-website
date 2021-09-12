from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from .models import Question, Choice

#Where question form attribuses are displyed with  question text being able for the admin user
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['html']
        widgets = {
            'html': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
        }

# Form for admin when selecting  multiple choice question
class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['html', 'is_correct']
        widgets = {
            'html': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
        }

# Class used to check if only one choice is selected within the admin page
class ChoiceInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(ChoiceInlineFormset, self).clean()

        correct_choices_count = 0
        for form in self.forms:
            if not form.is_valid():
                return

            if form.cleaned_data and form.cleaned_data.get('is_correct') is True:
                correct_choices_count += 1

        try:
            assert correct_choices_count == Question.ALLOWED_NUMBER_OF_CORRECT_CHOICES
        except AssertionError:
            raise forms.ValidationError(_('Exactly one correct choice is allowed.'))


User = get_user_model()