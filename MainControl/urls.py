"""MainControl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from django.contrib import admin
from django.shortcuts import render
from django.contrib.auth.views import *
from django.contrib.auth.views import LoginView
from signUp import views as signup_view
from dashBoard import views as dashboard_view
from loginPage import views as loginPage_view
from profilePage import views as profilePage_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.conf.urls import url, handler404
from Quiz import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('admin/', admin.site.urls),

    # Test Yourself Url path
    path('quiz/', views.mainQuiz, name='quiz'),

    # Url path for first MCQ quiz
    path('MCQ_quiz', views.play, name='MCQ_quiz'),
    path('MCQ/', views.quiz1, name='MCQ'),

    #  Url path for second sideshow quiz
    path('slideshow/', views.quiz2, name='sideshow'),
    path('slideshow_quiz/', views.play1, name='sideshow_quiz'),

    url(r'^submission-result/(?P<attempted_question_pk>\d+)/', views.submission_result, name='submission_result'),
    url(r'^submission-result1/(?P<attempted_question_pk>\d+)/', views.submission_result1, name='submission_result1'),

    # Views for main dashboard , news api and advice page
    path('', dashboard_view.newsApi, name='dashboard'),
    path('advice/', dashboard_view.adviceView, name='advice'),

    # Url paths for login ,signup , logout, and profile page
    path('login/', loginPage_view.loginPage, name="login"),
    path('logout/', loginPage_view.logoutUser, name="logout"),
    path('signUp/', signup_view.signUp, name="signup"),
    path('profile/', profilePage_view.profilePage, name="profile"),
    path('delete_account/', profilePage_view.deleteUser, name='delete_account'),

    # All the views for password page from email
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset_email.html"),
         name="reset_password"),  # submit email form
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_complete.html"),
         name="password_reset_confirm"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="resetPassword_done.html"),
         name="password_reset_done"),  # email sent success message
    # user id encoded in base 64
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="resetPassword_complete.html"),
         name="password_reset_complete"),  # password successfully changes message

    # Imports for icons acorss html pages
    url(r'^favicon\.ico$', RedirectView.as_view(url='static/images/favicon.ico')),
]


def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {})


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = custom_page_not_found_view
