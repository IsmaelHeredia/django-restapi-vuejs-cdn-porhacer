from django.urls import include, re_path
from django.urls import path, include
from .views import (
    TareaListApiView,
    TareaDetailApiView
)
from api import views

urlpatterns = [
    path('tareas', TareaListApiView.as_view()),
    path('tareas/<int:tarea_id>/', TareaDetailApiView.as_view()),
    path('tareas/enviar', views.enviarTareas),
]