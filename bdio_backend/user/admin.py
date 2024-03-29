from django.contrib import admin
from .models import User, TokenEmailConfirmation

admin.site.register(User)
admin.site.register(TokenEmailConfirmation)
