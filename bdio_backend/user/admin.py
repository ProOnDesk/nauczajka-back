from django.contrib import admin
from .models import User, TokenEmailConfirmation, User_Oauth2_Picture

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')  # Add 'id' to the list_display

admin.site.register(User, UserAdmin)
admin.site.register(TokenEmailConfirmation)
admin.site.register(User_Oauth2_Picture)
