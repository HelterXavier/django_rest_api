from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend.

    Allows users to log in using their email address or username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        # O SimpleJWT passa o USERNAME_FIELD (que é 'email') como 'username'.
        # Se o campo 'email' for passado diretamente, usamos ele.
        login_identifier = username or kwargs.get('email')
        if not login_identifier:
            return None
        try:
            # Try to fetch the user by matching the username or email field.
            user = UserModel.objects.get(
                Q(username__iexact=login_identifier) | Q(email__iexact=login_identifier))
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
