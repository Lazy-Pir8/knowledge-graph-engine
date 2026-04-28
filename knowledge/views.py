from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from knowledge.models import Topic, Games
from django.shortcuts import render, get_object_or_404
from .forms import TopicForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from django.contrib.auth.decorators import user_passes_test
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TopicSerializers
from rest_framework.response import Response


class HelloView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Hello, World'}
        return Response(content)

# Create your views here.
"""
class index(APIView):
     # permission_classes = (IsAuthenticated, )
    def get(self, request):
    # I don't know currently but later make index page to show list of knowledge items
        items = Topic.objects.all()
        serializer = TopicSerializers(items, many=True)
        return Response(serializer.data)
"""

def index(request):
    return render(request, "knowledge/index.html")

def weapons_index(request):
    # I don't know currently but later make index page to show list of knowledge items
    items = Topic.objects.all()
    return render(request, 'knowledge/index.html', {
        "items": items
    })

def games_index(request):
    # I don't know currently but later make index page to show list of knowledge items
    items = Games.objects.all()
    return render(request, 'knowledge/games_index.html', {
        "items": items
    })

def game_detail(request, slug):
    game = get_object_or_404(Games, slug=slug)

    return render(request, 'knowledge/game_detail.html', { 
        "game": game,
    })
    
@login_required(login_url='users:login')
def detail(request, slug):
    weapon = get_object_or_404(Topic, slug=slug)

    return render(request, 'knowledge/weapon_detail.html', { 
        "weapon": weapon,
    })

def is_editor(user):
    return user.groups.filter(name__in=['Editor']).exists()


@allowed_users(allowed_roles=['Admin', 'Editor'])
def add_weapon(request):
    if request.method == "POST":
        form = WeaponsForm(request.POST)
        if form.is_valid():

            weapon = form.save(commit=False)
            weapon.owner = request.user
            weapon.save()
            return redirect('knowledge:index')
        
    else:
        form = WeaponsForm()
    
    return render(request, 'knowledge/add_weapon.html', {
        'form': form
    })
@allowed_users(allowed_roles=['Admin', 'Editor'])
def add_game(request):
    if request.method == "POST":
        form = GamesForm(request.POST)
        if form.is_valid():

            game = form.save(commit=False)
            game.owner = request.user
            game.save()
            return redirect('knowledge:index')
        
    else:
        form = GamesForm()
    
    return render(request, 'knowledge/add_game.html', {
        'form': form
    })

def edit_weapon(request, slug):
    weapon = get_object_or_404(Topic, slug=slug)
    
  

    if request.user != weapon.owner and not request.user.groups.filter(name='Admin').exists():
        raise Http404("You do not have permission to edit this topic.")
    
    if request.method == "POST":
        form = WeaponsForm(request.POST or None, instance=weapon)
        if form.is_valid():
            form.save()

            return redirect('knowledge:detail', slug=weapon.slug,)
    else:
        form = WeaponsForm(instance=weapon)
        
        return render(request, 'knowledge/edit_weapon.html', {
            'form': form,
            'weapon': weapon
        })

def edit_game(request, slug):
    game = get_object_or_404(Games, slug=slug)
    
  

    if request.user != game.owner and not request.user.groups.filter(name='Admin').exists():
        raise Http404("You do not have permission to edit this topic.")
    
    if request.method == "POST":
        form = GamesForm(request.POST or None, instance=game)
        if form.is_valid():
            form.save()

            return redirect('knowledge:detail', slug=game.slug,)
    else:
        form = GamesForm(instance=game)
        
        return render(request, 'knowledge/edit_game.html', {
            'form': form,
            'game': game
        })


@allowed_users(allowed_roles=['Admin', 'Editor', 'User'])
def delete_weapon(request, slug):
    weapon = get_object_or_404(Weapons, slug=slug)
    if request.user != weapon.owner and not request.user.groups.filter(name='Admin').exists():
        raise Http404("You do not have permission to delete this weapon.")
    if request.method == "POST":
        weapon.delete()
        return redirect("knowledge:index")
    else:
        raise Http404("Weapon does not exist")



@allowed_users(allowed_roles=['Admin', 'Editor', 'User'])
def delete_game(request, slug):
    game = get_object_or_404(Games, slug=slug)
    if request.user != game.owner and not request.user.groups.filter(name='Admin').exists():
        raise Http404("You do not have permission to delete this game.")
    if request.method == "POST":
        game.delete()
        return redirect("knowledge:index")
    else:
        raise Http404("Game does not exist") 
