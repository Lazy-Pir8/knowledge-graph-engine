from django.urls import path    
from . import views

app_name = 'knowledge'
 
urlpatterns = [
    path('hello/', views.HelloView.as_view(), name='hello'),
    
    path('delete_topic/<slug:slug>/', views.delete_topic, name='delete_topic'),
    path('add_topic/', views.add_topic, name='add_topic'),
    path('edit_topic/<slug:slug>/', views.edit_topic, name='edit_topic'),
    path('<slug:slug>/', views.detail, name='detail'),
    path('', views.index.as_view(), name='index'),
    
    
]


