from random import randint

from dj_rest_auth.utils import jwt_encode
from django.contrib.auth import get_user_model
from rest_framework import generics, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from custom_auth.serializers import MyJWTSerializer
from user.serializers import MeSerializer


User = get_user_model()


class UserView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = MeSerializer
    permission_classes = [AllowAny]

    def __init__(self):
        super().__init__()
        self.user = None
        self.auth = None
        self.access_token = None
        self.refresh_token = None

    def get_object(self):
        pass

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.get_or_create_current_user()
        serializer_class = MyJWTSerializer

        if not self.auth:
            self.access_token, self.refresh_token = jwt_encode(self.user)
        else:
            refresh_token = RefreshToken.for_user(self.user)
            self.access_token = refresh_token.access_token
            self.refresh_token = refresh_token

        data = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
        }

        serializer = serializer_class(
            instance=data
        )

        response = Response(serializer.data)

        from dj_rest_auth.jwt_auth import set_jwt_cookies

        set_jwt_cookies(response, self.access_token, self.refresh_token)

        return response

    def get_or_create_current_user(self):
        self.auth = self.request.auth
        user = self.request.user
        email = ''

        if not self.auth:
            while True:
                try:
                    email = self.generate_anonymous_email()
                    User.objects.get(email=email)
                except User.DoesNotExist:
                    break

            user = User.objects.create_user(
                email,
                email,
                is_active=True,
                is_anonymous=True
            )

        self.user = user

    @staticmethod
    def generate_anonymous_email():
        random_number = ''.join(
            ["{}".format(randint(0, 9)) for num in range(0, 5)]
        )
        return f'anonymous{random_number}@gmail.com'
