from django.urls import path
from . import views

app_name = 'portfolio' # Boa prática para apps novas

urlpatterns = [
    path('', views.cursos_view, name='cursos'),
    path('pessoal/', views.pessoal_view, name='pessoal'),
    path('makingof/', views.makingof_view, name='makingof'),
    path('tfcs/', views.tfcs_view, name='tfcs'),
]