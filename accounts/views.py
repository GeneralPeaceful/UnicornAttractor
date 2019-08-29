from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.urls import reverse
from .forms import UserLoginForm, UserRegistrationForm

@login_required
def logout(request):
    """
    Logs the user out and redirects back to the home page
    """
    auth.logout(request)
    messages.error(request, 'You have successfully logged out.')
    return redirect(reverse('home'))


def login(request):
    """
    A view that manages the login form
    """
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in")
        return redirect('home')
    if request.method == 'POST':
        user_form = UserLoginForm(request.POST)
        if user_form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user:
                auth.login(request, user)
                messages.error(request, "You have successfully logged in")
                if request.GET and request.GET['next'] !='':
                    next = request.GET['next']
                    return HttpResponseRedirect(next)
                else:
                    return redirect(reverse('home'))
            else:
                user_form.add_error(None, "Your username or password are incorrect")
    else:
        user_form = UserLoginForm()

    args = {'user_form': user_form, 'next': request.GET.get('next', '')}
    return render(request, 'login.html', args)


def register(request):
    """
    A view that manages the registration form
    """
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in")
        return redirect('home')
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password1'))
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
