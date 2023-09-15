from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("Create New Page", views.create_page, name="create page"),
    path("Random Page", views.random_page, name="random"),
    path("Search", views.search, name="search"),
    path("Save <str:entry_title> Page", views.save_page),
    path("Edit <str:entry_title> Page", views.edit_page),
    path("<str:entry_title> Page Deleted", views.delete_page),
    path("<str:entry_title>", views.entry_page),
]

