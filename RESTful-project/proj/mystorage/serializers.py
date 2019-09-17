from .models import Essay, Album, Files
from rest_framework import serializers

class EssaySerializer(serializers.ModelSerializer):

    # 글쓴이를 자동적으로 등록함
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Essay
        # fields = '__all__'
        fields = ('pk', 'title' , 'body', 'author_name')

        # def perform_create(self, serializer):
        #     serializer.save(author = self.request.user)

class AlbumSerializer(serializers.ModelSerializer):

    # 글쓴이를 자동적으로 등록함
    author_name = serializers.ReadOnlyField(source='author.username')
    # 이미지를 업로드하고 결과값을 url로 하겠다
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = Album
        fields = ('pk', 'author_name' , 'image', 'desc')


class FilesSerializer(serializers.ModelSerializer):

    # 글쓴이를 자동적으로 등록함
    author_name = serializers.ReadOnlyField(source='author.username')
    myfile = serializers.FileField(use_url= True)

    class Meta:
        model = Files
        fields = ('pk', 'author_name' , 'myfile', 'desc')
