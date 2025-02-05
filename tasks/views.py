from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
                    return redirect('tasks')
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