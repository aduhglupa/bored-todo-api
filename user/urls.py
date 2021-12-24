from django.urls import path

from user.views import UserView


app_name = 'user'

urlpatterns = [
    path(
        'get-or-initiate-user', UserView.as_view(), name="get_or_initiate_user"
    )
]
