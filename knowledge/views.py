from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from knowledge.models import Topic
from django.shortcuts import render, get_object_or_404
from .forms import TopicForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from users.decorators import allowed_users
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
def index(request):
    # I don't know currently but later make index page to show list of knowledge items
    items = Topic.objects.all()
    return render(request, 'knowledge/index.html', {
        "items": items
    })

@login_required(login_url='users:login')
def detail(request, slug):
    topic = get_object_or_404(Topic, slug=slug)

    related_topics = Topic.objects.filter(tag = topic.tag).exclude(id=topic.id).order_by('-created_at')[:5]

    return render(request, 'knowledge/detail.html', { 
        "topic": topic,
        "related_topics":related_topics,
    })

def is_editor(user):
    return user.groups.filter(name__in=['Editor']).exists()


@allowed_users(allowed_roles=['Admin', 'Editor'])
def add_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():

            topic = form.save(commit=False)
            topic.owner = request.user
            topic.save()
            return redirect('knowledge:index')
        
    else:
        form = TopicForm()
    
    return render(request, 'knowledge/add_topic.html', {
        'form': form
    })

def edit_topic(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    
    print("Topic Found:", topic)

    if request.user != topic.owner and not request.user.groups.filter(name='Admin').exists():
        raise Http404("You do not have permission to edit this topic.")
    
    if request.method == "POST":
        form = TopicForm(request.POST or None, instance=topic)
        if form.is_valid():
            form.save()

            return redirect('knowledge:detail', slug=topic.slug,)
        
        return render(request, 'knowledge/edit_topic.html', {
            'form': form,
            'topic': topic
        })

@allowed_users(allowed_roles=['Admin', 'Editor', 'User'])
def delete_topic(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    if request.user != topic.owner and not request.user.groups.filter(name='Admin').exists():
        raise Http404("You do not have permission to delete this topic.")
    if request.method == "POST":
        topic.delete()
        return redirect("knowledge:index")
    else:
        raise Http404("Topic does not exist")
    
"""
def detail(request, name):
    name = name.lower()
    data = DATA_BY_NAME.get(name)
 
    if not data:
        return HttpResponse("Not Found")

    return render(request, 'knowledge/detail.html',{
        "name": data["name"].capitalize(),
        "description": data["description"]   
         
    })
"""

"""
DATA_BY_ID = {
    1: {"name": "Knowledge", "description": "Welcome to the Knowledge App!"},
    2: {"name": "linux", "description": "Linux is an open-source operatiThis is the first dataset.ng system modelled on UNIX."},
    3: {"name": "earth", "description": "Earth is the third planet from the Sun and the only astronomical object known to harbor life."},
}

DATA_BY_NAME = {
    "knowledge": {"name": "Knowledge", "description": "Welcome to the Knowledge App!"},
    "linux": {"name": "linux", "description": "Linux is an open-source operatiThis is the first dataset.ng system modelled on UNIX."},
    "earth": {"name": "earth", "description": "Earth is the third planet from the Sun and the only astronomical object known to harbor life."},
}
"""
'''
def knowledge_detail(request, id):    
    data = DATA_BY_ID.get(id)

    if not data:
        return HttpResponse("Not Found")
    return HttpResponse(data["description"])
'''
"""
def knowledge_detail(request,name):
    name = name.lower()
     
    data = DATA_BY_NAME.get(name)

    if not data:
        return HttpResponse("Not Found")
    return HttpResponse(data["description"])
"""