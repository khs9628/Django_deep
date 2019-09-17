---
title: ViewSet & Router
date: 2019-09-10 17:11:12
tags: Django
---

## ViewSet & Router

### Pagination

#### API 서버의 페이지네이션의 의의

하나의 request만으로 처리하기 어려운 레코드들을
여러 request로 나누어 전송

DRF (장고 Rest Framework)의 Pagination
1. **PageNumberPagination** - Default
2. LimitOffsetPagination
3. CusorPagination
4. **CustomizedPagination** 

```python
# Pagenation 설정 

# settings.py - 전역으로 설정 (Default)
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}
# views.py - 뷰단 별로 설정(CustomizedPagination)
from rest_framework import PageNumberPagination
class myPagination(PageNumberPagination)
    page_size = 100

class ViewSet(viewsets.ModelViewSet):
    queryset = UserPost.objects.all()
    serializer_class = UserSerializer
    pagination_class = myPagination
```

### Filtering vs Search ?

Filtering |Search  
:---: | :---:  
Request 걸러보내기 | Response 걸러보내기  

***cf) Request 가져오는법***

내용 | 명령어  
:---: | :---:  
내가 보낸 request | self.request  
내가보낸 request의 user | Self.request.user  
내가보낸 GET request | Self.request.GET (= self.request.query_param)  
내가보낸 POST request | self.request.POST 

### Authentication & Permission

***Authentication***  
서비스를 이용하는데 있어 내가 어느정도의 권한이 있음을  알려주는 과정
***Permission***    
서비스를 어느 정도로 이용할 수 있는지에 대한 권한


1. Authentication
    * BasicAuthentication
    HTTP 자체 기본인증에 기반한 인증방식
    HTTP 제어 헤더로 넘긴 ID, PW를 BASE64 ENCODING

    * TokenAuthentication
    인증요청 -> 유일한 key값을 발급

    * SessionAuthentication
    로그인이 될 때마다 저장되는 Session 정보를 참조하여 인증

    cf) Session을 관리하는 곳
    ``` python
    #settings.py
    MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    ]
    ```
    * RemoteUserAuthentication
    User정보가 다른 서비스에서 관리될 떄 사용되는 인증방식

```python
#settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}

# views.py
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

class ViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, 

```

2. Permission
    * AllowAny - default
    인증된 요청이든 비인증 요청이든 모든 허용하겠다.

    * IsAuthenticated
    인증된 요청에 대해서만 View 호출을 허용하겠다.

    * IsAdminUser
    Staff User에 대해서만 요청을 허용하겠다.

    * IsAuthenticatedOrReadOnly
    비인증요청에 대해서는 읽기만 허용하겠다.

    * ETC
    DjangoModelPermissions
    DjangoModelPermissionsORAnonReadOnly
    DjangoObjectPermissions

    
```python
#settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# views.py

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

class UserPostViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

#FBV -> decorator를 이용한 설정
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

@api_view({'GET'})
@permission_classes({'IsAuthenticated'})
def 함수명(request, format=None):
...
```

### Token Authentication
BasicAuthentication, SessionAuthentication의 한계
Mobile Client에 적합

#### 수행 과정
1. username, password와 1:1 매칭되는 고유 key 생성 / 발급
    * rest_framework/authtoken/views.py의 ObtaionAuthToken을 이용한 생성

    * Python 명렁어를 통한 생성
    ```bash
    python manage.py drf_create_token <username>
    # 강제로 재 생성
    python manage.py drf_create_token -r <username>
    ```
    * Signal을 이용한 Token 획득
    ```python
    from django.conf import settings
    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from rest_framework.authentication.models import Token

    #post_save = DB에 뭔가 저장된 직후에 특정 동작 수행
    @receiver(post_save, sender = settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance = None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)
    ```

2. 발급받은 Token을 API요청에 담아 인증을 처리
```bash
http POST http://127.0.0.1:8000/userpost/ "Authorization Token 토큰번호" title ="토큰글" body ="토큰내용"
```

### 실습

```python
#settings.py
# 1:1 매칭 -> OneToOneField를 이용해 Token을 발급
INSTALLED_APPS = [
    'rest_framework.authtoken'
]
#bash
python manage.py migrate
#현수 계정에 대한 토큰 생성
python manage.py drf_create_token hyunsoo

#urls.py
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
]
```
> 하루를 기록하다