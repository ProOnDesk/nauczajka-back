from user.models import User
from django.conf import settings
from typing import Union

def get_profile_image_with_ouath2(user: User) -> Union[str, None]:
    if hasattr(user, 'oauth2_picture') and user.oauth2_picture.view_picture and user.oauth2_picture.picture_url != "":
        return user.oauth2_picture.picture_url
    else:    
        return f"{settings.BACKEND_URL}{user.profile_image.url}" if user.profile_image else None