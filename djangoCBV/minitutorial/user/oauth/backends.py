# user/oauth/backends.py
# NaverBackend 백엔드는 기본인증백엔드(ModelBackend) 를 상속받아 대부분의 기능들을 그대로 사용

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AnonymousUser

UserModel = get_user_model()


class NaverBackend(ModelBackend):
    def authenticate(self, request, username=None,**kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            pass
        else:
            if self.user_can_authenticate(user):
                return user
