"""Forms module for the main app."""

from django.contrib.auth.forms import UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form."""

    class Meta(UserCreationForm.Meta):
        """Form metadata."""

        model = User
        fields = UserCreationForm.Meta.fields  # + ("custom_field",)

    def save(self, commit: bool = True) -> UserCreationForm:
        """Save user."""
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
