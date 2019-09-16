from rest_framework import viewsets
from .models import Essay , Album, Files
from .serializers import EssaySerializer, AlbumSerializer, FilesSerializer
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

# ModelViewSet 두가지 객체 - queryset / serializer_class
class PostViewSet(viewsets.ModelViewSet):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer

    # 검색 기능
    filter_backends = [SearchFilter]
    search_fields = ('title', 'body')

    # 현재 request를 보낸 유저
    # == self.request.user
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            qs = qs.filter(author= self.request.user)
        else:
            qs = qs.none()
        return qs

class ImgViewSet(viewsets.ModelViewSet):
    
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

# 다양한 미디어 파일을 받아야하기 때문에 지정해줘야함

class FileViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    
    # parser_class 지정
    parser_classes = (MultiPartParser, FormParser)

    # create() 오버라이딩 / API HTTP -> get() post() 오버라이딩
    def post(self, request, *arg, **kwargs):
        serializer = FilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_201_CREATED)
        
        else:
            return Response(serializer.error, status = HTTP_400_BAD_REQUEST)