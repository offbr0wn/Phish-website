from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateUserForm


# signup model for the web application uses django's library of authentication to validate the form
def signUp(request):
    if request.user.is_authenticated:  # Checks to see if user has already signed in
        return redirect('dashboard')  # returns the the main dashboard is user already signed in
    else:
        form = CreateUserForm()
        if request.method == 'POST':  # When submit button has  activated activates this if statement
            form = CreateUserForm(request.POST)

            if form.is_valid():  # If there all the information in the from , then the details ill be saved to the
                # database
                form.save()
                username = form.cleaned_data.get('username')

                messages.success(request, 'Account was created ' + username)
                return redirect('login')

        return render(request, 'register.html', {'form': form})
