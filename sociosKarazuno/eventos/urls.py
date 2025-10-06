from django.urls import path
from . import views

urlpatterns = [
    path("eventos/json", views.eventos_json, name="eventos_json"),
]
