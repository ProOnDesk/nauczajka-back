"""
User related models
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import EmailValidator


class UserManager(BaseUserManager):
    """
    Custom user manager
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a user
        """
        self.validate_email(email)

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and return a superuser
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
    def validate_email(self, email):
        """
        Validate email format
        """
        email_validator = EmailValidator(message='Please enter a valid email address.')
        email_validator(email)
    
    
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    """
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
