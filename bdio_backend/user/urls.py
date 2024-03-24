from django.urls import path, include
from .views import CreateUserView, ProfileUserView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]
