import random
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django_extensions.db.models import TimeStampedModel

###############################################################################################

# Classes for first quiz
class Question(TimeStampedModel):
    ALLOWED_NUMBER_OF_CORRECT_CHOICES = 1

    html = models.TextField(_('Question Text'))
    # is_published = models.BooleanField(_('Has been published?'), default=False, null=False)
    maximum_marks = models.DecimalField(_('Maximum Marks'), default=1, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.html


class Choice(TimeStampedModel):
    MAX_CHOICES_COUNT = 4  # Max of four choices displayed for quiz 1

    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    is_correct = models.BooleanField(_('Is this answer correct?'), default=False, null=False)
    html = models.TextField(_('Choice Text'))

    def __str__(self):
        return self.html


class QuizProfile(TimeStampedModel):
    # Sores user details and total score into variable
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.DecimalField(_('Total Score'), default=0, decimal_places=2,
                                      max_digits=10)  # max limited assigned to user is 10

    # Used when to override default name of the object of the class
    def __str__(self):
        return f'<QuizProfile: user={self.user}>'

    # Method used to get next question when user answered current one
    def get_new_question(self):
        # Will filter the queryset of the objects
        used_questions_pk = AttemptedQuestion.objects.filter(quiz_profile=self).values_list('question__pk', flat=True)
        remaining_questions = Question.objects.exclude(pk__in=used_questions_pk)

        # If there are no left question then will return it self , if not will randomise the questions and display
        # the next random question
        if not remaining_questions.exists():
            return
        return random.choice(remaining_questions)

    def create_attempt(self, question):
        # Assigned attempted question to variable where question and quiz_profile is passed thought  allowing to
        # access attributes of the method in the class
        attempted_question = AttemptedQuestion(question=question, quiz_profile=self)
        attempted_question.save()

    def evaluate_attempt(self, attempted_question, selected_choice):
        if attempted_question.question_id != selected_choice.question_id:
            return

        attempted_question.selected_choice = selected_choice
        if selected_choice.is_correct is True:
            attempted_question.is_correct = True
            # gets the marks if question is right and assigns and adds up the score to maximum marks
            attempted_question.marks_obtained = attempted_question.question.maximum_marks

        attempted_question.save()
        self.update_score()


    # Updates users score by using django functions to filter and sum up the marks
    def update_score(self):
        marks_sum = self.attempts.filter(is_correct=True).aggregate(
            models.Sum('marks_obtained'))['marks_obtained__sum']
        self.total_score = marks_sum or 0
        self.save()


class AttemptedQuestion(TimeStampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz_profile = models.ForeignKey(QuizProfile, on_delete=models.CASCADE, related_name='attempts')
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(_('Was this attempt correct?'), default=False, null=False)
    marks_obtained = models.DecimalField(_('Marks Obtained'), default=0, decimal_places=2, max_digits=6)

    def get_absolute_url(self):
        return f'/submission-result/{self.pk}/'


##############################################################################################################
# Classes for quiz 2
# Classes are same as first quiz , but added hint and image field
class Question1(TimeStampedModel):
    ALLOWED_NUMBER_OF_CORRECT_CHOICES = 1

    html = models.TextField(_('Question Text'))
    is_published = models.BooleanField(_('Has been published?'), default=False, null=False)
    maximum_marks = models.DecimalField(_('Maximum Marks'), default=1, decimal_places=2, max_digits=6)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    hint = models.TextField(default="There is no hint for this Question")

    def __str__(self):
        return self.html


#
class Choice1(TimeStampedModel):
    MAX_CHOICES_COUNT = 2  # Only two option available

    question = models.ForeignKey(Question1, related_name='choices', on_delete=models.CASCADE)
    is_correct = models.BooleanField(_('Is this answer correct?'), default=False, null=False)
    html = models.TextField(_('Choice Text'))

    def __str__(self):
        return self.html


class slideshow(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score1 = models.DecimalField(_('Total Score'), default=0, decimal_places=2, max_digits=10)

    def __str__(self):
        return f'<slideshow: user={self.user}>'  # Returns quiz 2 profile with the related user

    # this will get a new question formwhic the admin had assigend
    def get_new_question(self):
        used_questions_pk = AttemptedQuestion1.objects.filter(quiz_profile=self).values_list('question__pk', flat=True)
        remaining_questions = Question1.objects.exclude(pk__in=used_questions_pk)
        if not remaining_questions.exists():
            return
        return random.choice(remaining_questions) # will display the question in a random order

    def create_attempt(self, question):
        attempted_question = AttemptedQuestion1(question=question, quiz_profile=self)
        attempted_question.save()
#WIll check to see if the question that the user selected matches he correct answer
    def evaluate_attempt(self, attempted_question1, selected_choice):
        if attempted_question1.question_id != selected_choice.question_id:
            return

        attempted_question1.selected_choice = selected_choice
        if selected_choice.is_correct is True:
            attempted_question1.is_correct = True
            attempted_question1.marks_obtained = attempted_question1.question.maximum_marks

        attempted_question1.save()
        self.update_score()

    def update_score(self):
        marks_sum = self.attempts.filter(is_correct=True).aggregate(
            models.Sum('marks_obtained'))['marks_obtained__sum']
        self.total_score1 = marks_sum or 0
        self.save()


class AttemptedQuestion1(TimeStampedModel):
    question = models.ForeignKey(Question1, on_delete=models.CASCADE)
    quiz_profile = models.ForeignKey(slideshow, on_delete=models.CASCADE, related_name='attempts')
    selected_choice = models.ForeignKey(Choice1, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(_('Was this attempt correct?'), default=False, null=False)
    marks_obtained = models.DecimalField(_('Marks Obtained'), default=0, decimal_places=2, max_digits=6)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    hint = models.TextField(default="There is no hint for this Question")

    def get_absolute_url(self):
        return f'/submission-result1/{self.pk}/'
