from django.urls import path
from .views import CreateUserView, ProfileUserView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('profile/', ProfileUserView.as_view(), name='profile'),
]
