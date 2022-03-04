from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .managers import CustomUserManager


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = None
    email = models.EmailField(_("email address"), unique=True, max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def blacklist_outstanding_tokens(self):
        tokens = self.outstandingtoken_set.values_list("token", flat=True)

        for token in tokens:
            try:
                token = RefreshToken(token)
            except (TokenBackendError, TokenError):
                pass
            else:
                token.blacklist()


class UserAgentHistory(models.Model):
    user = models.ForeignKey(User, related_name="user_agents", on_delete=CASCADE)
    agent = models.TextField(blank=True)
    logged_in = models.DateTimeField(auto_now_add=True)
