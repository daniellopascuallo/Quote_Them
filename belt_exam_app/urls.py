from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("registration", views.registration),
    path("login", views.login),
    path("quotes", views.quotes),
    path("add_quote", views.add_quote),
    path("logout", views.logout),
    path("user/<int:userID>", views.user_quotes),
    path("like_quote/<int:quoteID>", views.like_quote),
    path("delete_quote/<int:quoteID>", views.delete_quote),
    path("edit/<int:userID>", views.edit_account),
    path("edit/<int:userID>/update", views.update_account)
]
