from rest_framework.routers import DefaultRouter
from mystorage import views
from django.urls import path, include
from rest_framework import urls

# DefaultRouter기반의 라우터 등록 
router = DefaultRouter()

router.register('essay', views.PostViewSet)
router.register('album', views.ImgViewSet)
router.register('files', views.FileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
