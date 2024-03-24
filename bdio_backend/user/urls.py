from django.urls import path, include
from .views import CreateUserView, ProfileUserView, ConfirmUserView
from django_rest_passwordreset.urls import reset_password_request_token, reset_password_confirm

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('confirm_user/',ConfirmUserView.as_view(), name='confirm_user')
]
