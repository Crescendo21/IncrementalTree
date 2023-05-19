from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('diagram/', views.diagram, name='diagram'),
    path('result/', views.result, name='result'),
    path('generate_ideas/', views.generate_ideas, name='generate_ideas'),
]
