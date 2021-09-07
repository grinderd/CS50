from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("entrysearch", views.entrysearch, name="entrysearch"),
    path('editentry', views.editentry, name='editentry'),
    path('updateentry', views.updateentry, name='updateentry'),
    path('random', views.randomentry, name='random'),
    path("<str:title>", views.entry, name="title")

]
