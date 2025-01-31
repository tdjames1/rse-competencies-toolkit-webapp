"""Models module for the main app."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for this project."""


class Category(models.Model):
    """Model for categories."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    parent_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )


class SkillLevel(models.Model):
    """Model for skill levels."""

    name = models.CharField(max_length=50)
