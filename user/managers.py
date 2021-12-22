from allauth.account.models import EmailAddress
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email must be set'))

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_anonymous', False)

        user = self.create_user(email, password, **extra_fields)

        # Set super user to verified email
        email_address = EmailAddress.objects.add_email(None, user, email)
        email_address.verified = True
        email_address.primary = True
        email_address.save()

        return user
