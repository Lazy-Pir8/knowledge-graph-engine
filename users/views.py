from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm 
from django.contrib.auth.decorators import login_required
from users.decorators import unaunthenticated_user, allowed_users
from django.contrib.auth.models import Group

# Create your views here.

@login_required(login_url='users:login')
@allowed_users(allowed_roles=['Admin', 'Editor'])
def index(request):
    return render(request, 'users/user.html')

@unaunthenticated_user
def register(request):
    
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        user = form.save() 

        group = Group.objects.get(name="Editor")
        user.groups.add(group)

        user.save()

    return render(request, 'users/register.html', {
        "form": form
    })


@unaunthenticated_user
def login_view(request): 
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("users:index"))
        else:
            return render(request, 'users/login.html', {
                "message": "Invalid Credentials"
            })

    return render(request, 'users/login.html', {
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("users:login"))