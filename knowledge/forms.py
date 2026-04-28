from django import forms
from django.forms import ModelForm 
from .models import Topic, Games

class WeaponsForm(ModelForm):
    class Meta:
        model = Topic
        fields = ["name", "description"]

class GamesForm(ModelForm):
    class Meta:
        model = Games
        fields = ["name", "description"]