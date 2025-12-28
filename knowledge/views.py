from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from knowledge.models import Topic
from django.shortcuts import render, get_object_or_404
from .forms import TopicForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


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

    return render(request, 'knowledge/detail.html', { 
        "topic": topic,
    })

def add_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('knowledge:index')
    else:
        form = TopicForm()
    
    return render(request, 'knowledge/add_topic.html', {
        'form': form
    })

def delete_topic(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
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