"""Test suite for the main views.

This test module includes tests for main views of the app ensuring that:
  - The correct templates are used.
  - The correct status codes are returned.
"""

from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from .view_utils import LoginRequiredMixin


def test_index(client):
    """Test the index view is routed to the correct template."""
    with assertTemplateUsed(template_name="main/index.html"):
        response = client.get("/")
    assert response.status_code == HTTPStatus.OK


def test_privacy(client):
    """Test the privacy page view is routed to the correct template."""
    with assertTemplateUsed(template_name="main/privacy.html"):
        response = client.get("/privacy/")
    assert response.status_code == HTTPStatus.OK


@pytest.mark.xfail
class TestCreateUserView(LoginRequiredMixin):
    """Test suite for the CreateUserView."""

    def _get_url(self):
        return reverse("create_user")

    def test_get(self, client):
        """Test the view GET request uses the correct template."""
        with assertTemplateUsed(template_name="main/create_user.html"):
            response = client.get(self._get_url())
        assert response.status_code == HTTPStatus.OK
