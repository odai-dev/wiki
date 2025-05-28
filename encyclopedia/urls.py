from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.view_page, name="entry"),
    path("new", views.new_entry, name="new")
    
]
