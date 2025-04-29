"""Urls module for the main app."""

from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("privacy/", views.privacy, name="privacy"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
]
