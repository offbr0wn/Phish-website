from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import QuizProfile, AttemptedQuestion, slideshow, AttemptedQuestion1
from itertools import chain


################################################################################
# Views for  quiz pages

# View for main quiz page when directed to 'Test yourself'
@login_required(login_url='login')
def mainQuiz(request):
    # Leaderboard function where the user highscore is created and displayed on the leaderboard within the quiz page
    top_quiz_profiles = QuizProfile.objects.order_by('-total_score')[:500]
    total_count = top_quiz_profiles.count()
    context = {'top_quiz_profiles': top_quiz_profiles, 'total_count': total_count, }
    return render(request, 'testYourself.html', context=context)


# View for MCQ quiz Card
@login_required(login_url='login')
def quiz1(request):
    return render(request, 'quiz1.html', {})


def quiz2(request):
    return render(request, 'slideshow_rules_quiz2.html', {})


##################################################################################


#####################################################################################
# Main function of  MCQ quiz
@login_required(login_url='login')
def play(request):
    quiz_profile, created = QuizProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Retrieves question_pk from html page when form is submitted
        question_pk = request.POST.get('question_pk')
        # Will return a queryset that is a foreign key relationship
        attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=question_pk)

        # Gets the choice field in html
        choice_pk = request.POST.get('choice_pk')

        try:
            # Goes through the queryset to find the choices within the question model
            selected_choice = attempted_question.question.choices.get(pk=choice_pk)
        except ObjectDoesNotExist:  # Otherwise will raise exception when no object is found
            raise Http404
        # Calls the evalute_attempt class to pass through pk for both question and choice
        quiz_profile.evaluate_attempt(attempted_question, selected_choice)

        return redirect(attempted_question)

    else:
        question = quiz_profile.get_new_question()
        if question is not None:  # if question is there it will  pass the question variable to display new question
            quiz_profile.create_attempt(question)

        context = {
            'question': question,
        }

        return render(request, 'Quiz_to_do.html', context=context)


# Displays correct answer  when user submitted their choice
def submission_result(request, attempted_question_pk):
    attempted_question = get_object_or_404(AttemptedQuestion, pk=attempted_question_pk)

    context = {
        'attempted_question': attempted_question,

    }

    return render(request, 'submission_result.html', context=context)


# ###############################################################################################################
# Main function for second quiz being spotting the phished emails , this method is excalty same as the first quiz
# however the model for the method takes in a hint , image field which it then displayed to the user. Once user has
# submitted the quiz will check if there are any new unanswered quiz next if not will redirect user back to main
# quiz page
@login_required(login_url='login')
def play1(request):
    quiz_profile, created = slideshow.objects.get_or_create(user=request.user)
    # Checks to see if the form has been submitted
    if request.method == 'POST':
        # looks for 'question_pk ' within the html file , stores the question number in a variable
        question_pk = request.POST.get('question_pk')

        attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=question_pk)

        choice_pk = request.POST.get('choice_pk')

        try:
            selected_choice = attempted_question.question.choices.get(pk=choice_pk)
        except ObjectDoesNotExist:
            raise Http404  # Returns error if condition is not met

        quiz_profile.evaluate_attempt(attempted_question, selected_choice)

        return redirect(attempted_question)

    else:
        question = quiz_profile.get_new_question()
        if question is not None:
            quiz_profile.create_attempt(question)

        context = {
            'question': question,
        }

        return render(request, 'slideshow_quiz2.html', context=context)


# Shows correct answer on new template for slideshow quiz
def submission_result1(request, attempted_question_pk):
    attempted_question = get_object_or_404(AttemptedQuestion1, pk=attempted_question_pk)
    context = {
        'attempted_question': attempted_question,
    }

    return render(request, 'submission_result.html', context=context)
