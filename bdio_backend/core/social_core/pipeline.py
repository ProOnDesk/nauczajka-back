"""
https://python-social-auth.readthedocs.io/en/latest/configuration/django.html
"""

from user.models import User_Oauth2_Picture

USER_FIELDS = ["username", "email"]

def custom_create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {"is_new": False}
    
    fields = {
        name: kwargs.get(name, details.get(name))
        for name in backend.setting("USER_FIELDS", USER_FIELDS)
    }

    if not fields:
        return

    return {"is_new": True, "user": strategy.create_user(is_confirmed=True, is_oauth2=True **fields)}

def get_avatar_picture(backend, strategy, details, response,
        user=None, *args, **kwargs):
    url = None
    if kwargs['is_new'] == True:
        User_Oauth2_Picture.objects.create(user=user)

    if backend.name == 'google-oauth2':
        url = response.get('picture', None)
    
    if url is not None:
        user_google = User_Oauth2_Picture.objects.get(user=user)

        if user_google.view_picture == True:
            user_google.picture_url = url
            user_google.save()
        
        

