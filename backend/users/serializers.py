from os import write
from unittest.mock import Base
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'instruments',
                  'photo', 'is_active', 'is_staff', 'created_at', 'updated_at']


class MeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'email', 'instruments', 'photo']

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value


class UserCreateSerializer(serializers.ModelSerializer):
    passwor = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def validate_email(self, email):
            if User.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError(
                    "This email is already in use.")
            return email

        def validated_username(self, username):
            if User.objects.filter(username__iexact=username).exists():
                raise serializers.ValidationError(
                    "This username is already in use.")
            return username

        def create(self, validated_data):
            validated_data.pop('password2')
            return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True,
                                         required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError(
                {"new_password": "New passwords must match."})
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return {"detail": "Password updated successfully."}
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Você pode adicionar claims customizadas ao token aqui, se desejar
        return token
