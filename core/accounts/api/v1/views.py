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
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import jwt


class RegistrationApiView(generics.GenericAPIView):
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
        refresh = RefreshToken.for_user(user)
        return(str(refresh.access_token))


class CustomObtainAuthToken(ObtainAuthToken):
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordAPIView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
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
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class EmailTesting(generics.GenericAPIView):
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
    def get(self, request, token, *args, **kwargs):
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
        refresh = RefreshToken.for_user(user)
        return(str(refresh.access_token))
    
class EmailResetPasswordView(generics.GenericAPIView):
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
