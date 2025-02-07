from django.urls import path
from . import views

urlpatterns = [
    path( '', views.home, name = "home" ),
    path( 'signup/', views.signup, name = "signup" ),
    path( 'tasks/', views.tasks, name = "tasks"),
    path( 'logout/', views.signout, name = "logout"),
    path( 'signin/', views.signin, name = "signin"),
    path( 'create_task/', views.create_task, name = "create_task")
]