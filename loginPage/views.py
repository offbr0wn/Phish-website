from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


# Main Function for login page
def loginPage(request):
    context = {}  # Empty dictionary with variable names as a key
    if request.user.is_authenticated:  # Checks to see if user has previously signed in then redirects to dashboard
        return redirect('dashboard')
    else:  # If user not logged in previously then will go to check details with the account user has created in sql
        # database
        if request.method == "POST":  # Once submit in form has been submitted activates if statement

            # Grabs  name and stores  in variable in  login.html for username and password field
            username = request.POST.get('username')
            password = request.POST.get('password')
            # uses django inbuilt library to verify password and username by taking two arguments
            user = authenticate(request, username=username, password=password)
            if user is not None:  # if user is there
                login(request, user)  # Saves user's ID from the authenticated user
                return redirect('dashboard')
            else:
                messages.info(request,
                              'Username of password incorrect  ')  # If info entered wrong displays error message

                # context['error'] = "Login wrong"

    return render(request, 'login.html', context)


# Method when called in , logout the user from the session and cleans data completely
def logoutUser(request):
    logout(request)
    messages.info(request, "Logged out successfully!  ")
    return redirect('login')
