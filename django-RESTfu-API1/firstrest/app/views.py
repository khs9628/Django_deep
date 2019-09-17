from rest_framework import viewsets
from .models import Post
from .serializer import PostSerializer
from rest_framework import renderers
##action Decorator
from rest_framework.decorators import action
from django.http import HttpResponse

#CBV

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # @action(method=['post'])
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # 그녕 TEXT를 띄우는 CUSTOM API
    def highlight(self, request, *args, **kwargs):
        return HttpResponse("Text")