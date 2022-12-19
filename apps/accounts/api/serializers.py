from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate
from apps.accounts.models import UserProfile
from django.utils.encoding import force_str
from rest_framework import serializers
from rest_framework import status


class RegisterSerializer(serializers.ModelSerializer):
    confirm = serializers.CharField(max_length=70, required=True, write_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'email', 'last_name', 'first_name',
            'phone_number', 'password', 'confirm'
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm = attrs.get('confirm')
        email = attrs.get('email')

        if password != confirm:
            raise serializers.ValidationError('Password did not match')

        user_exists = UserProfile.objects.filter(email=email).first()

        if user_exists:
            raise serializers.ValidationError('User exist please try again!')

        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        phone_number = validated_data['phone_number']
        password = validated_data['password']
        hashed_password = make_password(password)

        user = UserProfile.objects.create(

            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            password=hashed_password,

        )

        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=150, write_only=True)
    confirm = serializers.CharField(max_length=150, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        confirm = attrs.get('confirm')

        if password == confirm:
            user_exists = authenticate(requests=self.context.get('request'),
                                       email=email, password=password)

            if not user_exists:
                msg = 'User does not definite, \n wrong username or password'
                raise serializers.ValidationError(msg, code=status.HTTP_403_FORBIDDEN)

        else:
            raise serializers.ValidationError('Password or confirm incorrect! please try again')

        attrs['user'] = user_exists
        return attrs


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150, required=True, write_only=True)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=70, write_only=True, required=True
    )
    confirm = serializers.CharField(
        min_length=6, max_length=70, write_only=True, required=True
    )
    token = serializers.CharField(
        max_length=600, write_only=True, required=True
    )
    uidb64 = serializers.CharField(
        max_length=20, write_only=True, required=True
    )

    class Meta:
        fields = ['password', 'confirm', 'token', 'uidb64']

    def validate(self, attrs):

        password = attrs.get('password')
        confirm = attrs.get('confirm')
        token = attrs.get('token')
        uidb64 = attrs.get('uidb64')
        _id = force_str(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(id=_id)
        current_password = user.password

        if not PasswordResetTokenGenerator().check_token(user=user, token=token):
            raise AuthenticationFailed('The reset link invalid', 401)

        if password != confirm:
            raise serializers.ValidationError('confirm password does not match', code=status.HTTP_400_BAD_REQUEST)

        if check_password(password, current_password):
            raise serializers.ValidationError(
                {'success': False, 'message': 'New password should not similar to current password'})

        user.set_password(password)
        user.save()

        return super().validate(attrs)


class UpdateProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'image_url',
            'email',
            'phone_number',
            'address',
            'bio'
        ]
