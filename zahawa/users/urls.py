from django.urls import path
from . import views


# User Authentication related routes
urlpatterns = [
    path("profile/", views.User.as_view()),
    path("signup/", views.UserRegister.as_view()),
    path("login/", views.UserAuth.as_view()),
    path("email_verification/", views.EmailVerification.as_view()),
    path("reset_password/", views.UserPasswordReset.as_view()),
    path("password/update/", views.UserPasswordUpdate.as_view()),
    path("password/change/", views.ChangePassword.as_view()),

]
