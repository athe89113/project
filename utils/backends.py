# coding: utf-8
from django.contrib.auth import get_user_model


class EmailAuthBackend(object):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair, then check
    a username/password pair if email failed


    **注意** 此类不能编译，因为 django.contrib.auth 中会判断此类的类型，编译之后无法识别为 python function
    """

    def authenticate(self, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(username=username)
                if user.check_password(password):
                    return user
            except UserModel.DoesNotExist:
                return None
        except UserModel.MultipleObjectsReturned:
            return None

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
