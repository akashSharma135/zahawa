from django.http import JsonResponse
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from users import models
from users.models import CustomUser
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.contrib.auth.hashers import make_password


# --------------------------------User Register Serializer--------------------------------


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:

        model = CustomUser
        fields = ("email","password","name", "phone_number")

    def create(self, validated_data):
        email = validated_data.pop("email", None)
        password = validated_data.pop("password", None)
        user = CustomUser.objects.create(
            email=email, password=make_password(password), **validated_data
        )
        return user
        # is called if we save serializer if it have an instance

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance



class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password"]


# --------------------------------User Get Data Serializer--------------------------------


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"



# --------------------------------User Register Serializer--------------------------------


class RegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=250, required=False)
    phone_number = serializers.CharField(max_length=250, required=False)

    def get_cleaned_data(self):
        super(RegisterSerializer, self).get_cleaned_data()
        return {
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
            "email": self.validated_data.get("email", ""),
            "full_name": self.validated_data.get("full_name", ""),
            "phone_number": self.validated_data.get("phone_number", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.phone_number = self.validated_data.get("phone_number", "")
        user.full_name = self.validated_data.get("full_name", "")
        user.save()
        return user


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Otp
        fields = ["code"]


# --------------------------------User Password Reset Serializer--------------------------------


class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email"]




