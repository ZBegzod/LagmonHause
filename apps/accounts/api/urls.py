from django.urls import path
from .views import (
    LoginApiView,
    RegisterApiView,
    SetPasswordApiView,
    ProfileUpdateApiView,
    PasswordTokenCheckAPI,
    EmailVerificationApiView,
    ResetPasswordEmailRequest,
)

urlpatterns = [

    # authentications by email
    path('register', RegisterApiView.as_view()),
    path('login', LoginApiView.as_view()),
    path('email-verification/<token>', EmailVerificationApiView.as_view(), name='verify-email'),

    # password reset by email
    path('password-reset-email', ResetPasswordEmailRequest.as_view()),
    path('password-reset-confirm/<token>/<uidb64>', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetPasswordApiView.as_view(), name='password-reset-complete'),

    # user update profile
    path('update-profile/<int:pk>', ProfileUpdateApiView.as_view()),


]
