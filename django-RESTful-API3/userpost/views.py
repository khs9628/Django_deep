from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from userpost.models import UserPost
from userpost.serializer import UserSerializer
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

class UserPostViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = UserPost.objects.all()
    serializer_class = UserSerializer

    filter_backends = [SearchFilter]
    search_fields = ('title', 'body',)
    # 어떤 칼럼을 기반으로 검색할 건지?

    def get_queryset(self):
        # 여기 내부에서 쿼리셋을 가져와라
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            # 로그인한 유저의 글만 filtering 해라
            qs = qs.filter(author=self.request.user)
        else:
            # 로그인 안되어있다면 -> 비어있는 쿼리셋을 반환해라.
            qs = qs.none()
        return qs

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)