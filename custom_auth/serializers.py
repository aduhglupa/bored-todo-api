from django.conf import settings
from django.utils.translation import gettext as _
from dj_rest_auth.serializers import JWTSerializer, LoginSerializer
from rest_framework import exceptions, serializers


class MyLoginSerializer(LoginSerializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = self.get_auth_user(None, email, password)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user)

        attrs['user'] = user
        return attrs

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class MyJWTSerializer(JWTSerializer):
    user = None

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
