from django.contrib import admin
from .models import User, TokenEmailConfirmation

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')  # Add 'id' to the list_display

admin.site.register(User, UserAdmin)
admin.site.register(TokenEmailConfirmation)
