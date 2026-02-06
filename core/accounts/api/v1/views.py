from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
from django.shortcuts import get_object_or_404
from django.conf import settings
from mail_templated import EmailMessage

from accounts.models import User, Profile
from .serializers import (
    RegistrationSerializers,
    CustomAuthTokenSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    CustomTokenObtainPairSerializer,
    ActivationResendSerializer,
    EmailResetPasswordSerializer,
    ResetPasswordSerializer,
)
from .utils import EmailThread
import jwt


class RegistrationApiView(generics.GenericAPIView):
    """
    Post user with email and password
    Check validations
    Create user
    Send an email for user with jwt token

    """
    serializer_class = RegistrationSerializers

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token_for_user(user_obj)
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@admin.com', [email])
            EmailThread(email_obj).start()
            data = {"email": email}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def get_token_for_user(self, user):
        """
        create a jwt token for user
        """
        refresh = RefreshToken.for_user(user)
        return(str(refresh.access_token))


class CustomObtainAuthToken(ObtainAuthToken):
    """
    Create token with user credentials
    Response contain token, user id and email of user
    """
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    """
    Destroying auth token
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordAPIView(generics.GenericAPIView):
    """
    API endpoint for authenticated users to change their own password.
    Expects old_password and new_password in request data.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Return the currently authenticated user.
        This view does not support changing passwords for other users.
        """
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        """
        Validates old password and updates user's password if valid.
        """
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(
                serializer.validated_data["old_password"]
            ):
                return Response(
                    {"detail": "Wrong password!"}, status=status.HTTP_400_BAD_REQUEST
                )
            self.object.set_password(serializer.validated_data["new_password"])
            self.object.save()
            return Response(
                {"detail": "Password change successfuly!"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for Authenticated users to get own profile.
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Get currently user object
        If user not exist return 404
        """
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Create jwt token for sender user
    Expects email and password in request data.
    """
    serializer_class = CustomTokenObtainPairSerializer

class EmailTesting(generics.GenericAPIView):
    """
    Just for testing email operation
    """
    def get(self, request, *args, **kwargs):
        user_obj = get_object_or_404(User, email='user@gmail.com')
        token = self.get_token_for_user(user_obj)
        email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@admin.com', ['user@gmail.com'])
        EmailThread(email_obj).start()
        return Response('email sent')
    
    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return(str(refresh.access_token))
    
class ActivationAPIView(APIView):
    """
    API endpoint for users who received verification email to going to verify own account.

    """
    def get(self, request, token, *args, **kwargs):
        """
        A GET request for decode jwt token.
        Checking Token validations.
        Turn is_verified fields of user's account to True and save if pass
        """
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except ExpiredSignatureError:
            return Response({'detail': 'Token has been expired!'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({'detail': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response({'detail': 'Invalid Token Header'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_obj = User.objects.get(pk = user_id)

        if user_obj.is_verified:
            return Response({'details': 'Your account has already been verfied!'}, status=status.HTTP_200_OK)
        user_obj.is_verified = True
        user_obj.save()
        return Response({'details': 'Users email is verfied!'}, status=status.HTTP_200_OK)
    
class ActivationResendAPIView(generics.GenericAPIView):
    """
    API Endpoint for resend activation email for users
    Sending email with jwt token
    """
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user_obj']
        token = self.get_token_for_user(user_obj)
        email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@admin.com', [user_obj.email])
        EmailThread(email_obj).start()
        return Response({'details': 'User activation resend successfuly!'}, status=status.HTTP_200_OK)
    
    def get_token_for_user(self, user):
        """
        Build and return access token for current user
        """
        refresh = RefreshToken.for_user(user)
        return(str(refresh.access_token))
    
class EmailResetPasswordView(generics.GenericAPIView):
    """
    First Step for reset user password by sending email to
    user's email.
    The url for get new password build with jwttoken.
    """
    serializer_class = EmailResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data['user_obj']
        token = self.get_token_for_user(user_obj)
        email_obj = EmailMessage('email/reset_password_email.tpl', {'token': token}, 'admin@admin.com', [user_obj.email])
        EmailThread(email_obj).start()
        return Response({'details': 'Email sent successfuly!'}, status=status.HTTP_200_OK)
    
    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return(str(refresh.access_token))
    
class ResetPasswordView(generics.GenericAPIView):
    """
    Second step for reseting user's password.
    Expects new_password and new_password1 in request data.
    """
    serializer_class = ResetPasswordSerializer

    def put(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except ExpiredSignatureError:
            return Response({'detail': 'Token has been expired!'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({'detail': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)
        except DecodeError:
            return Response({'detail': 'Invalid Token Header'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = User.objects.get(pk = user_id)
        user_obj.set_password(serializer.validated_data["new_password"])
        user_obj.save()
        return Response(
                {"detail": "Password change successfuly!"}, status=status.HTTP_200_OK
        )
