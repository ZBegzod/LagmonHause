from rest_framework.response import Response
from apps.accounts.models import UserProfile
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth import login
from django.conf import settings
from django.urls import reverse
from drf_yasg import openapi
from .utils import Util

from rest_framework import (
    status, views, generics
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from django.contrib.auth.tokens import (
    PasswordResetTokenGenerator
)

from django.utils.encoding import (
    smart_bytes, smart_str,
    DjangoUnicodeDecodeError
)

from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode
)

from django.contrib.sites.shortcuts import (
    get_current_site
)

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    SetNewPasswordSerializer,
    UpdateProfileModelSerializer,
    ResetPasswordEmailRequestSerializer
)
import jwt


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = UserProfile.objects.filter(email=user_data['email']).first()

        current_site = get_current_site(request=request).domain
        relative_link = reverse('verify-email', kwargs={'token': str(user.tokens['access'])})
        abs_url = f'http://{current_site}{relative_link}'
        email_body = f'Hi, {user.email} \n User link below to activate your email \n {abs_url}'

        data = {
            'email_subject': 'Activate email',
            'email_body': email_body,
            'to_email': user.email,
        }

        Util.send_email(data=data)
        return Response({'success': 'We have sent you link to register our website'}, status=status.HTTP_201_CREATED)


class LoginApiView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return Response(user.tokens, status=status.HTTP_202_ACCEPTED)


class ResetPasswordEmailRequest(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        email = request.data['email']

        if UserProfile.objects.filter(email=email).exists():
            user = UserProfile.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))

            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'token': token, 'uidb64': uidb64})
            abs_url = 'http://' + current_site + relative_link
            email_body = 'Hello \n Use link below to reset your password \n ' + abs_url

            data = {

                'email_subject': 'Reset your password',
                'email_body': email_body,
                'to_email': user.email

            }

            Util.send_email(data)
        return Response({'success': 'We have sent you link to reset your password'}, status=status.HTTP_200_OK)


class EmailVerificationApiView(views.APIView):
    permission_classes = [AllowAny]
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Verify email',
                                           type=openapi.TYPE_STRING)

    def get(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = UserProfile.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'success': True, 'message': 'Email successfully activated',
                             'token': str(user.tokens['access'])
                             }, status=status.HTTP_200_OK)
        except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError) as e:
            return Response({'success': False, 'message': f'Verification expired | {e.args}'},
                            status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, token, uidb64):
        try:
            _id = smart_str(urlsafe_base64_decode(uidb64))
            user = UserProfile.objects.get(id=_id)

            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                return Response({'error': 'Token is not valid, please request a new  one'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({'success': True, 'message': 'Credentials Valid', 'token': token, 'uidb64': uidb64})

        except DjangoUnicodeDecodeError as error:
            return Response({'success': False, 'message': f'DecodeError: {error.args}'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetPasswordApiView(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = SetNewPasswordSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset successfully'}, status=status.HTTP_200_OK)


class ProfileUpdateApiView(generics.RetrieveUpdateAPIView):
    serializer_class = UpdateProfileModelSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        query = self.get_object()
        if query:
            serializer = self.get_serializer(query)
            return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'message': 'query did not exist'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        object = self.get_object()
        serializer = self.serializer_class(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': serializer.data}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'success': True, 'message': 'credentials is invalid'}, status=status.HTTP_404_NOT_FOUND)


