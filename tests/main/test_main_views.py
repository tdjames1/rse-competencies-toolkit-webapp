"""Test suite for the main views.

This test module includes tests for main views of the app ensuring that:
  - The correct templates are used.
  - The correct status codes are returned.
"""

from http import HTTPStatus

from pytest_django.asserts import assertTemplateUsed


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
