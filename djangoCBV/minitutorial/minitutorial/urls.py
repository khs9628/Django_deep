# minitutorial/urls.py

from django.contrib import admin
from django.urls import path

from django.contrib.auth.views import LogoutView
from bbs.views import ArticleListView, ArticleDetailView, ArticleCreateUpdateView
from user.views import UserRegistrationView, UserLoginView, UserVerificationView, ResendVerifyEmailView, SocialLoginCallbackView

urlpatterns = [
    path('article/', ArticleListView.as_view()),
    path('article/create/', ArticleCreateUpdateView.as_view()),
    path('article/<article_id>/', ArticleDetailView.as_view()),
    path('article/<article_id>/update/', ArticleCreateUpdateView.as_view()),
    
    path('user/create/', UserRegistrationView.as_view()), # 회원가입
    path('user/login/', UserLoginView.as_view()),         # 로그인
    path('user/logout/', LogoutView.as_view()),
    path('user/<pk>/verify/<token>/', UserVerificationView.as_view()),
    path('user/resend_verify_email/', ResendVerifyEmailView.as_view()),
    path('user/login/social/<provider>/callback/', SocialLoginCallbackView.as_view()),

    path('admin/', admin.site.urls),
]