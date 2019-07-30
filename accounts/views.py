from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.urls import reverse
from .forms import UserLoginForm, UserRegistrationForm


def logout(request):
    """
    Logs the user out and redirects back to the home page
    """
    auth.logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect(reverse('home'))


def login(request):
    """
    A view that manages the login form
    """
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        user_form = UserLoginForm(request.POST)
        if user_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            if username == '' or password == '':
                messages.error(request, 'Please enter your login credentials.')
                return redirect('login')
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, "You have successfully logged in.")
                if request.GET and request.GET['next'] !='':
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('home'))
            else:
                user_form.add_error(None, "Your username or password are incorrect.")
                return redirect('login')
    else:
        user_form = UserLoginForm()
    args = {'user_form': user_form, 'next': request.GET.get('next', '')}
    return render(request, 'login.html', args)


@login_required
def profile(request):
    """
    A view that displays the profile page of a logged in user
    """
    return render(request, 'profile.html')


def register(request):
    """
    A view that manages the registration form
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()

            user = auth.authenticate(request.POST.get('email'),
                                     password=request.POST.get('password1'))

            if user:
                auth.login(request, user)
                messages.success(request, "You have successfully registered")
                return redirect(reverse('home'))

            else:
                messages.error(request, "unable to log you in at this time!")
    else:
        user_form = UserRegistrationForm()

    args = {'user_form': user_form}
    return render(request, 'register.html', args)
