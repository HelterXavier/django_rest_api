from django.urls import path
from .views import UserView, UserPasswordView, LogoutView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)

urlpatterns = [
    path('users/', UserView.as_view(), name='user_account'),
    path('users/password/', UserPasswordView.as_view(), name='update_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
