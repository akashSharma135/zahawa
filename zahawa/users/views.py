from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from . import models
from drf_yasg import openapi
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from rest_framework.authtoken.models import Token
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from random import randint
from rest_framework import permissions


def random_with_N_digits():
    range_start = 10 ** (6 - 1)
    range_end = (10 ** 6) - 1
    return randint(range_start, range_end)


# --------------------------------User Register View--------------------------------


class UserRegister(APIView):
    def get_serializer(self):
        return serializers.UserRegisterSerializer()

    def post(self, request):
        email = request.data.get("email")
        phone = request.data.get("phone_number")
        if email is not None:
            isemail = CustomUser.objects.filter(email=email)
            if isemail:
                data = {"message": "This email is already registered", "field": "email"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if phone is not None:
            isphone = CustomUser.objects.filter(phone_number=phone)
            if isphone:
                data = {
                    "message": "This phone number is already registered",
                    "field": "phone",
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json["token"] = token.key
                email = str(user)
                try:
                    subject = "Please Verify your Email"
                    otp = random_with_N_digits()
                    email_message = (
                        "Hi, <br><br> Please Verify your Email by below Otp: <br><br>"
                        + str(otp)
                    )
                    send_mail(
                        subject,
                        email_message,
                        getattr(settings, "EMAIL_HOST_USER"),
                        [email],
                        fail_silently=False,
                    )
                    user_check = models.Otp.objects.filter(email=email)
                    if user_check:
                        user_check.update(code=otp)
                    else:
                        models.Otp.objects.create(email=email, code=otp)

                except BadHeaderError:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                return Response(
                    {
                        "key": token.key,
                        "message": "A  email verification otp has been sent",
                    },
                    status=status.HTTP_201_CREATED,
                )
        else:
            data = {"error": True, "errors": serializer.errors}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class EmailVerification(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self):
        return serializers.OtpSerializer()

    def post(self, request):
        code = request.data.get("code")
        try:
            otp_check = models.Otp.objects.get(email=request.user.email)
        except Exception:
            data = {"error": True, "message": "User Otp Doesn't exists"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if str(otp_check.code) == str(code):
            CustomUser.objects.filter(email=request.user.email).update(verified=True)
            data = {"error": False, "message": "Otp successfully verified"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {"error": True, "message": "Otp is not correct please try again"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


# --------------------------------User Login View--------------------------------


class UserAuth(APIView):
    def get_serializer(self):
        return serializers.UserLoginSerializer()

    def post(self, request):
        isemail = CustomUser.objects.filter(email=request.data.get("email"))
        if not isemail:
            data = {
                "message": "Account with this email does not exist",
                "field": "email",
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        if not isemail[0].is_active:
            data = {
                "message": "your account is not activated",
                "field": "email",
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if user is not None:
            try:
                token = Token.objects.get(user_id=user.id)
            except:
                token = Token.objects.create(user=user)
            return Response({"key": token.key, "message": "Login Successful"})
        else:
            data = {
                "field": "password",
                "message": "This password is incorrect, please try again",
            }

            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


# --------------------------------User Password Reset View--------------------------------


class UserPasswordReset(APIView):
    def get_serializer(self):
        return serializers.PasswordResetSerializer()

    def post(self, request):
        if request.method == "POST":
            email = request.data.get("email")
            if email is not None:
                User = get_user_model()
                associated_users = User.objects.filter(Q(email=email))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Password Reset Requested"
                        email_template_name = "password/password_reset_email.txt"
                        c = {
                            "email": user.email,
                            "domain": "127.0.0.1:8000",
                            "site_name": "Website",
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            "token": default_token_generator.make_token(user),
                            "protocol": "http",
                        }
                        domain = (
                            str(request.scheme) + "://" + str(request.META["HTTP_HOST"])
                        )
                        email = render_to_string(email_template_name, c)
                        email = email.replace(":baseurl:", "" + str(domain) + "")
                        try:
                            send_mail(
                                subject,
                                email,
                                getattr(settings, "EMAIL_HOST_USER"),
                                [user.email],
                                fail_silently=False,
                            )
                        except BadHeaderError:
                            return Response(status=status.HTTP_400_BAD_REQUEST)
                        return Response(
                            {
                                "status": "password reset mail sent please check your email"
                            }
                        )
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserPasswordUpdate(APIView):
    def get_serializer(self):
        properties = {
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="string"),
            "old_password": openapi.Schema(
                type=openapi.TYPE_STRING, description="string"
            ),
            "new_password1": openapi.Schema(
                type=openapi.TYPE_STRING, description="string"
            ),
            "new_password2": openapi.Schema(
                type=openapi.TYPE_STRING, description="string"
            ),
        }
        return_openapi_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT, properties=properties
        )
        return return_openapi_schema

    def post(self, request):
        email = request.data.get("email")
        try:
            User = get_user_model()
            userDetails = User.objects.get(email=email)
        except Exception:
            data = {"error": True, "message": "User dose not exists with this email"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("new_password1") != request.data.get("new_password2"):
            data = {
                "field": "new_password1",
                "message": "Password1 and Password2 should be same",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        randompass = request.data.get("new_password1")
        userDetails.password = make_password(randompass)
        userDetails.save()
        data = {"error": False, "message": "Password changed successfully"}
        return Response(data, status=status.HTTP_200_OK)


# --------------------------------User Change Password View--------------------------------


class ChangePassword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer(self):
        properties = {
            "old_password": openapi.Schema(
                type=openapi.TYPE_STRING, description="string"
            ),
            "new_password1": openapi.Schema(
                type=openapi.TYPE_STRING, description="string"
            ),
            "new_password2": openapi.Schema(
                type=openapi.TYPE_STRING, description="string"
            ),
        }
        return_openapi_schema = openapi.Schema(
            type=openapi.TYPE_OBJECT, properties=properties
        )
        return return_openapi_schema

    def post(self, request):
        email = request.user.email
        try:
            User = get_user_model()
            userDetails = User.objects.get(email=email)
        except Exception:
            data = {"error": True, "message": "User dose not exists with this email"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get("new_password1") != request.data.get("new_password2"):
            data = {
                "field": "new_password1",
                "message": "Password1 and Password2 should be same",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if not userDetails.check_password(request.data.get("old_password")):
            data = {
                "field": "old_password",
                "message": "Old Password doesn't match",
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        randompass = request.data.get("new_password1")
        userDetails.password = make_password(randompass)
        userDetails.save()
        data = {"error": False, "message": "Password changed successfully"}
        return Response(data, status=status.HTTP_200_OK)


# --------------------------------Get User Data View--------------------------------


class User(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserSerializer(
            models.CustomUser.objects.get(pk=request.user.id)
        )
        return Response(serializer.data)

    def get_serializer(self):
        return serializers.UserSerializer()

    def patch(self, request):
        objects = models.CustomUser.objects.filter(email=request.user.email).first()
        serializer = serializers.UserSerializer(
            objects, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
