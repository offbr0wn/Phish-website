from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import CustomerForm, ImageChangeForm
from .forms import UserDeleteForm


@login_required(login_url='login')
def profilePage(request):
    # Variable created to store class form for image , User and password form
    form = CustomerForm(request.POST, instance=request.user.profile)
    pic_form = ImageChangeForm(request.POST, request.FILES, instance=request.user.profile)
    password = PasswordChangeForm(request.user, request.POST)
    if request.method == 'POST':
        if 'form1' in request.POST:  # If button with name 'form1 ' will activate CustomerForm
            if form.is_valid():
                form.save()  # Once changes to form have been made saves information into database
                messages.success(request, f'Your account is updated ')
                return redirect('profile')  # Once condition is met ,redirects to profile page

            # Will active this condition is User  changes profile page
        elif 'form2' in request.POST:
            if pic_form.is_valid():
                pic_form.save()
                messages.success(request, f'Your account is updated ')
                return redirect('profile')

        elif 'form3' in request.POST:
            if password.is_valid():
                user = password.save()
                # Important! as takes users hashed password and saves with new password in hash form
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the error below.')



    else:
        form = CustomerForm(request.POST, instance=request.user.profile)
        pic_form = ImageChangeForm(request.POST, instance=request.user.profile)
        password = PasswordChangeForm(request.user)

    context = {'form': form, 'pic_form': pic_form, 'password': password}

    return render(request, 'Newprofile.html', context)


# Method is called from url.py when  user goes to delete account
@login_required(login_url='login')
def deleteUser(request):
    # Checks to see if user has submitted the form
    if request.method == 'POST':

        user = request.user
        user.delete()  # Retrieves current user logged in  , using django to delete user from database
        messages.info(request, 'Your account has been deleted.')
        return redirect('login')
    else:
        delete_form = UserDeleteForm(instance=request.user)

    context = {'delete_form': delete_form}

    return render(request, 'delete_account.html', context)
