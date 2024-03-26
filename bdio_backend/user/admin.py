from django.contrib import admin
from .models import User, TokenEmailConfirmation, Tutor

admin.site.register(User)
admin.site.register(TokenEmailConfirmation)
admin.site.register(Tutor)