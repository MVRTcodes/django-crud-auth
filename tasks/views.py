from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid :
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('home')
                except:
                    return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        'error': 'Username already exists.'
                    })
            else:
                return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        'error': 'Password do not match.'
                    })
        else:
            return render(request, 'signup.html', {
                        'form': UserCreationForm,
                        'error': 'Form not valid.'
                    })
        
def tasks(request):
    return render(request, 'tasks.html')

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        form = AuthenticationForm(request.POST)
        if form.is_valid:
            try:
                user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
                if User is None:
                    render(request, 'signin.html', {
                        'form': AuthenticationForm,
                        'error': 'User or password is incorrect.'
                    })
                else:
                    login(request, user)
                    return redirect('home')
            except:
                render(request, 'signin.html', {
                    'form': AuthenticationForm,
                    'error': 'Wrong password, try again.'
                })
        else:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Could not login, form is not valid.'
            })
