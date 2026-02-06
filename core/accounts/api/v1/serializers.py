from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core import exceptions
from ...models import User, Profile


class RegistrationSerializers(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        """
        Match checking for password and password1
        Chaeck password validation
        Raise errors if checking were failed
        """
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError(
                {"detail": "Passwords doesnt match!"})

        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)

    def create(self, validated_data):
        """
        Remove password1 field from form
        Create user with given email and password
        """
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    """
    Get email and password from request
    Validate and return credentials
    """
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        """
        Checking request which include email and password
        Checking exiting user
        Checking is_verified field
        """
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError(
                    {"details": "User is not verified!"})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer responsible for validating password change input.
    Ensures password confirmation, diffrence from old password,
    and compliance with Django password validations rules.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Cross-fields validation for password change.
        """
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError(
                {"detail": "Passwords doesnt match!"})

        if attrs.get("new_password") == attrs.get("old_password"):
            raise serializers.ValidationError(
                {"detail": "New password must be different with old password!"}
            )

        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile model plus email field
    """
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "image",
            "description"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Just override the validate method
    and adding email and user id to response
    """
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["email"] = self.user.email
        validated_data["id"] = self.user.id
        return validated_data

class ActivationResendSerializer(serializers.Serializer):
    """
    Serializer for resend activation email by getting
    email from user
    """
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        """
        Get user object if exist
        Send User object in attrs
        """
        email = attrs.get('email')
        try:
            user_obj = get_object_or_404(User, email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "details": "User does not exits!"
            })
        attrs['user_obj'] = user_obj
        return super().validate(attrs)
    
class EmailResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for reset password with sending email by getting
    email from user
    """
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user_obj = get_object_or_404(User, email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "details": "User does not exits!"
            })
        attrs['user_obj'] = user_obj
        return super().validate(attrs)
    
class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer responsible for validating password reset input.
    Ensures password confirmation, diffrence from old password,
    and compliance with Django password validations rules.
    """
    new_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Cross-fields validation for reset password.
        """
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError(
                {"detail": "Passwords doesnt match!"})

        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)