# bbs/views.py - CBV(Class Based View)

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView
from bbs.models import Article

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from django.conf import settings


class ArticleListView(TemplateView):
    template_name = 'article_list.html'    # 뷰 전용 템플릿 생성.
    queryset = None

    def get(self, request, *args, **kwargs):
        print(request.GET)
        ctx = {
            'view': self.__class__.__name__, # 클래스의 이름
            'articles': self.get_queryset()
        }
        return self.render_to_response(ctx)

    def get_queryset(self):
        if not self.queryset:
            self.queryset = Article.objects.all()
        return self.queryset


class ArticleDetailView(TemplateView):       # 게시글 상세
    template_name = 'article_detail.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'                 # 검색데이터의 primary key를 전달받을 이름

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset     # queryset 파라미터 초기화
        pk = self.kwargs.get(self.pk_url_kwargs) # pk는 모델에서 정의된 pk값, 즉 모델의 id
        return queryset.filter(pk=pk).first()    # pk로 검색된 데이터가 있다면 그 중 첫번째 데이터 없다면 None 반환

        if not article:
            raise Http404('invalid pk')
        return article

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        
        ctx = {
            'view': self.__class__.__name__, # 클래스의 이름
            'article': article
        }
        return self.render_to_response(ctx)

@method_decorator(csrf_exempt, name='dispatch')   # 모든 핸들러 예외 처리
class ArticleCreateUpdateView(TemplateView):  # 게시글 추가, 수정
    login_url = settings.LOGIN_URL       # 설정파일의 값으로 설정
    template_name = 'article_update.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        article = queryset.filter(pk=pk).first()

        if pk:
            if not article:
                raise Http404('invalid pk')
            elif article.author != self.request.user:                             # 작성자가 수정하려는 사용자와 다른 경우
                raise Http404('invalid user')
        return article

    def get(self, request, *args, **kwargs):
        article = self.get_object()
        
        ctx = {
            'article': article
        }
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')           # request.POST 객체에서 데이터 얻기
        post_data = {key: request.POST.get(key) for key in ('title', 'content')} # 작성자를 입력받지 않도록 수정
        for key in post_data:                         # 세가지 데이터 모두 있어야 통과
            if not post_data[key]:
                messages.error(self.request, '{} 값이 존재하지 않습니다.'.format(key), extra_tags='danger') # error 레벨로 메시지 저장
        
        post_data['author'] = self.request.user

        if len(messages.get_messages(request)) == 0:                  # 메시지가 있다면 아무것도 처리하지 않음
            if action == 'create':  # action이 create일 경우
                article = Article.objects.create(**post_data)
                messages.success(self.request, '게시글이 저장되었습니다.')  # success 레벨로 메시지 저장
            elif action == 'update': # action이 update일 경우
                article = self.get_object()
                for key, value in post_data.items():
                    setattr(article, key, value)
                article.save()
                messages.success(self.request, '게시글이 성공적으로 수정되었습니다.', extra_tags='info')  # info 레벨로 메시지 저장
            else: # action이 없거나 create, update 중 하나가 아닐 경우
                messages.error(self.request, '알 수 없는 요청입니다.', extra_tags='danger')     # error 레벨로 메시지 저장
            
            return HttpResponseRedirect('/article/') # 정상적인 저장이 완료되면 '/articles/'로 이동됨
        
        ctx = {
            'article': self.get_object() if action == 'update' else None
        }
        return self.render_to_response(ctx)
        
