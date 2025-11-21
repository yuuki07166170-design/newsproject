from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    title = models.CharField(verbose_name='カテゴリ', max_length=20)

    def __str__(self):
        return self.title

class NewsPost(models.Model):
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT,
    )

    title = models.CharField(verbose_name='タイトル', max_length=200)
    comment = models.TextField(verbose_name='コメント')
    image1 = models.ImageField(verbose_name='イメージ1', upload_to='newses')
    image2 = models.ImageField(verbose_name='イメージ2', upload_to='newses', blank=True, null=True)
    posted_at = models.DateTimeField(verbose_name='投稿日', auto_now_add=True)
    
    def __str__(self):
        return self.title

# コメント機能：ニュース投稿に対するコメントを保存するモデル
class Comment(models.Model):
    # どのニュース投稿に対するコメントか
    news_post = models.ForeignKey(NewsPost, verbose_name='ニュース投稿', on_delete=models.CASCADE, related_name='comments')
    # コメントしたユーザー
    user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
    # コメントの内容
    content = models.TextField(verbose_name='コメント内容')
    # コメントした日時
    posted_at = models.DateTimeField(verbose_name='投稿日時', auto_now_add=True)

    def __str__(self):
        return self.content[:20]

    class Meta:
        # 新しいコメントが上に来るように並び替え
        ordering = ['-posted_at']
