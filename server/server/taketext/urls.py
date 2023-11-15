from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("gen", views.generate_voiceover, name="gen"),
    path("test", views.test, name="test"),
]
