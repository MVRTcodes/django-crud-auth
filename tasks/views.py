from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import TaskForm
from. models import Task
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
        
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    datecompleted__isnull=True
    return render(request, 'tasks/tasks.html',{
        'title':'Pending Tasks',
        'tasks': tasks
    })

def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    #datecompleted__isnull=True
    return render(request, 'tasks/tasks.html',{
        'title':'Completed Tasks',
        'tasks': tasks
    })

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {
            'form': TaskForm
        })
    else:
        print(request.POST)
        form = TaskForm(request.POST)
        if form.is_valid:
            try:
                new_task = form.save(commit=False)
                new_task.user = request.user
                print(new_task.save())
                return redirect('tasks')
            except ValueError:
                return render(request, 'tasks/create_task.html', {
                    'form': TaskForm,
                    'error': 'Please provide valid data.'
                })
        else:
            return render(request, 'tasks/create_task.html', {
                'form': TaskForm,
                'error': 'Form not valid.'
            })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user = request.user)
        form = TaskForm(instance=task)
        return render(request, 'tasks/task_detail.html', {
            'task': task,
            'form' : form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user = request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/task_detail.html', {
            'task': task,
            'form' : form,
            'error': 'Error updating task.'
        })

@login_required
def complete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
      

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
         