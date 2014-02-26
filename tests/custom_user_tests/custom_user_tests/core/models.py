"""Replace the django.contrib.auth User with our CustomUser.
This file can also be used as a base for creating your own custom user model.
"""
from django.contrib.auth import models as auth
from django.db import models


class CustomUserManager(auth.BaseUserManager):
    """A custom user manager that uses email addresses for usernames.
    """
    def create_user(self, email, password):
        """Create a user with their email address.
        """
        email = self.normalize_email(email)

        user = self.model(email=email)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create the superuser and make them active by default.
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(auth.PermissionsMixin, auth.AbstractBaseUser):
    """A custom user that uses the email address as their username.
    This model contains the minimal set of fields for a useful CustomUser
    model that uses emails to login.
    """
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def get_username(self):
        """Return the email username.
        This method is used in Django, and djregs depends on it for custom user
        models.
        """
        return getattr(self, self.USERNAME_FIELD)
