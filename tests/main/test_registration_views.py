"""Test suite for the registration views."""

from http import HTTPStatus

import pytest
from django.core import mail
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed


@pytest.fixture
def password_reset_uid_and_token(client, user):
    """Returns the uid and token for password reset."""
    response = client.post(reverse("password_reset"), data={"email": user.email})
    token = response.context[0]["token"]
    uid = response.context[0]["uid"]

    return uid, token


@pytest.fixture
def password_reset_url(password_reset_uid_and_token):
    """Returns the password reset URL."""
    uid, token = password_reset_uid_and_token
    return reverse("password_reset_confirm", kwargs={"uidb64": uid, "token": token})


@pytest.fixture
def set_password_url(client, password_reset_uid_and_token, password_reset_url):
    """Returns the set password URL."""
    uid, _ = password_reset_uid_and_token
    client.get(password_reset_url)
    return reverse(
        "password_reset_confirm", kwargs={"uidb64": uid, "token": "set-password"}
    )


class TestPasswordReset:
    """Test suite for the password_reset views."""

    def _get_url(self):
        return reverse("password_reset")

    def test_get(self, client):
        """Test the view GET request uses the correct template."""
        with assertTemplateUsed(template_name="registration/password_reset_form.html"):
            response = client.get(self._get_url())
        assert response.status_code == HTTPStatus.OK

    def test_post(self, client, user):
        """Test the view POST request redirects correctly."""
        # Request a password reset email
        response = client.post(self._get_url(), data={"email": user.email})

        # Assert redirects to password_reset/done
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse("password_reset_done")

    def test_password_reset_email_and_subject(
        self, client, user, password_reset_url, set_password_url
    ):
        """Test the password reset email and subject templates."""
        # Verify the generated email against the expected templates
        with open("main/templates/registration/password_reset_subject.txt") as f:
            expected_email_subject = f.read()
        with open("main/templates/registration/password_reset_email.html") as f:
            expected_email_content = f.read()
            # Replace template variables
            expected_email_content = expected_email_content.replace(
                "{{ email }}", user.email
            )
            expected_email_content = expected_email_content.replace(
                "{{ protocol }}", "http"
            )
            expected_email_content = expected_email_content.replace(
                "{{ domain }}", "testserver"
            )
            expected_email_content = expected_email_content.replace(
                "{% url 'password_reset_confirm' uidb64=uid token=token %}",
                password_reset_url,
            )

        assert len(mail.outbox) == 1
        generated_email = mail.outbox[0]
        assert generated_email.subject, expected_email_subject.strip()
        assert generated_email.body.strip(), expected_email_content.strip()

        # Now we can use the token to get the password change form
        response = client.get(password_reset_url)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == set_password_url


class TestPasswordResetDone:
    """Test suite for the password_reset_done views."""

    def test_password_reset_done(self, client):
        """Test the password_reset_done view."""
        with assertTemplateUsed(template_name="registration/password_reset_done.html"):
            response = client.get("/accounts/password_reset/done/")
        assert response.status_code == HTTPStatus.OK


class TestPasswordResetConfirm:
    """Test suite for the password_reset_confirm views."""

    def test_get(self, client, set_password_url):
        """Test the view GET request uses the correct template."""
        # Expect out custom error page if an incorrect token/uid is used
        with assertTemplateUsed(
            template_name="registration/password_reset_confirm.html"
        ):
            response = client.get(
                reverse(
                    "password_reset_confirm",
                    kwargs={"token": "some", "uidb64": "thing"},
                )
            )
        assert response.status_code == HTTPStatus.OK
        assertContains(response, "Password reset failed")

        # Expect our custom password_reset_confirm page
        with assertTemplateUsed(
            template_name="registration/password_reset_confirm.html"
        ):
            response = client.get(set_password_url)
        assert response.status_code == HTTPStatus.OK
        assertNotContains(response, "Password reset failed")


class TestPasswordResetComplete:
    """Test suite for the password_reset_complete views."""

    def _get_url(self):
        return reverse("password_reset_complete")

    def test_get(self, client):
        """Test the view GET request uses the correct template."""
        # Expect our custom password_reset_complete page
        with assertTemplateUsed(
            template_name="registration/password_reset_complete.html"
        ):
            response = client.get(self._get_url())
        assert response.status_code == HTTPStatus.OK

    def test_password_reset_complete(self, client, set_password_url):
        """Test the password_reset_complete view."""
        # Set the new password
        # Note that this needs to be sufficiently strong to be accepted
        response = client.post(
            set_password_url,
            data={
                "new_password1": "bkjbkjwdnwqkldnwkjfdnqlkecf",
                "new_password2": "bkjbkjwdnwqkldnwkjfdnqlkecf",
            },
        )
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == self._get_url()
