from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view_page, name="entry"),
    path("new", views.new_entry, name="new"),
    path("wiki/<str:title>/edit", views.edit_page, name="edit"),
    path("wiki/", views.random_page, name="random")
]
