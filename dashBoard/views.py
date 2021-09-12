from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from newsapi import NewsApiClient
from django.shortcuts import get_object_or_404
#
# from .forms import QuizForm

from django.contrib import messages

# Create your views here.
from Quiz.models import QuizProfile, slideshow


@login_required(login_url='login')

# Function called for news api ,searches and retriees live articles from  web.
def newsApi(request):
    # Api used to unique identifier  to authenticate a user
    newsapi = NewsApiClient(api_key="e5d53569982f49398117ec59e2df2048")
    # Folters out articles by top headlines , showing from specific news outlets
    topheadlines = newsapi.get_everything(q='phishing',
                                          sources='bbc-news,the-verge',

                                          language='en',

                                         )
    articles = topheadlines['articles']
    # Empty array
    desc = []
    news = []
    img = []
    # Iterates through loop to display img, title and description of news
    for i in range(2):
        myarticles = articles[i]

        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
    highscore = QuizProfile.objects.get_or_create(user=request.user)

    mylist = zip(news, desc, img)
    # Takes the request form the form , with template name producing http response of template
    return render(request, 'dashboard1.html', context={"mylist": mylist, 'highscore': highscore}
                  )
# Function where view is rendered out for advice page, where path is called from url.py by activating the method
@login_required(login_url='login')
def adviceView(request):
    context = {}
    return render(request, 'advice.html', context)
