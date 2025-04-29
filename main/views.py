"""Views for the main app."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


def index(request: HttpRequest) -> HttpResponse:
    """View that renders the index/home page.

    Args:
      request: A GET request.
    """
    return render(request=request, template_name="main/index.html")


def privacy(request: HttpRequest) -> HttpResponse:
    """View that renders the privacy page.

    Args:
      request: A GET request.
    """
    return render(request=request, template_name="main/privacy.html")


def register(request: HttpRequest) -> HttpResponse:
    """View that renders the user registration form page.

    Args:
      request: An HTTP request.
    """
    if request.method == "POST":
        user_form = CustomUserCreationForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect("login")
    else:
        user_form = CustomUserCreationForm()
    return render(request, "registration/create_user.html", {"user_form": user_form})
