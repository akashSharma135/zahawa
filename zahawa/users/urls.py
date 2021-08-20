from django.urls import path
from . import views


# User Authentication related routes
urlpatterns = [
    path("register/", views.UserRegister.as_view()),
]
