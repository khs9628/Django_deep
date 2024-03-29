from django.db import models
from django.utils import timezone

class Article(models.Model):
    title      = models.CharField('타이틀', max_length=126, null=False)
    content    = models.TextField('내용', null=False)
    # author     = models.CharField('작성자', max_length=16, null=False)
    author     = models.ForeignKey('user.User', related_name='articles', on_delete=models.CASCADE)
    created_at = models.DateTimeField('작성일', default=timezone.now)


    def __str__(self):
        return '[{}] {}'.format(self.id, self.title)