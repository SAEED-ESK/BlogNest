from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extrafields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Eamil must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extrafields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extrafields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extrafields.setdefault("is_superuser", True)
        extrafields.setdefault("is_staff", True)
        extrafields.setdefault("is_active", True)
        extrafields.setdefault("is_verified", True)

        if extrafields.get("is_staff") is not True:
            raise ValueError(_("SuperUser Must have is_staff=True."))
        if extrafields.get("is_superuser") is not True:
            raise ValueError(_("SuperUser Must have is_superuser=True."))

        return self.create_user(email, password, **extrafields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def display_name(self):
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return full_name or self.user.email

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    Create a profile for user after user be created
    """
    if created:
        Profile.objects.create(user=instance)
