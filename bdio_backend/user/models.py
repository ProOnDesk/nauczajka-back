"""
User related models
"""
from os import path as os_path

import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from django.conf import settings

from django.core.validators import EmailValidator
from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

def get_upload_user_path(instance, filename):
    ext = os_path.splitext(filename)[1]
    filename = f'{instance.id}{ext}'

    return os_path.join('uploads', 'user',  filename)


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
        user.is_confirmed = True
        user.save(using=self._db)
        return user
    
    def create_tutor(self, email, password, **extra_fields):
        """
        Create and return a tutor
        """
        user = self.create_user(email, password, **extra_fields)
        user.is_tutor = True
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
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_staff = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to=get_upload_user_path, blank=True, null=True, default=os_path.join('uploads', 'user', 'default.jpg'))
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
        """
        Handles password reset tokens
        When a token is created, an e-mail needs to be sent to the user
        :param sender: View Class that sent the signal
        :param instance: View Instance that sent the signal
        :param reset_password_token: Token Model Object
        :param args:
        :param kwargs:
        :return:
        """
        
        reset_password_url = f"{settings.FRONTED_URL}/account/reset-password/?reset_token={reset_password_token.key}"
        
        # send an e-mail to the user
        context = {
            'reset_password_url': reset_password_url,
        }

        # render email text
        email_html_message = render_to_string('core/user_reset_password_email.html', context)
        email_plaintext_message = strip_tags(email_html_message)

        msg = EmailMultiAlternatives(
            # title:
            "Resetowanie hasla",
            # message:
            email_plaintext_message,
            # from:
            settings.DEFAULT_FROM_EMAIL,
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
        
    def __str__(self):
        return self.email


class TokenEmailConfirmation(models.Model):
    """
    Token email account confirmation model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    # created_at_int = models.IntegerField()
    
    def __str__(self):
        return self.token


class User_Oauth2_Picture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='oauth2_picture')
    view_picture = models.BooleanField(default=True)
    picture_url = models.URLField(default="")
    