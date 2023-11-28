from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, Model, ForeignKey, SET_NULL, BooleanField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from omnihr_assignment.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for omnihr-assignment.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore
    company = ForeignKey('Company', related_name='user_company', null=True, on_delete=SET_NULL)
    is_active = BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Company(Model):
    name = CharField(null=True, blank=True, max_length=255)
    description = CharField(null=True, blank=True, max_length=255)
