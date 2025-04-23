from django.urls import path
from user.views import create_user

urlpatterns = [
    path("", create_user, name="user-create"),
]
