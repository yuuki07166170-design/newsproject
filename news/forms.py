from django.forms import ModelForm
from .models import NewsPost, Comment

class NewsPostForm(ModelForm):
    class Meta:
        model = NewsPost
        fields = ['category', 'title', 'comment', 'image1', 'image2']

# コメント機能：コメント投稿用のフォーム
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        # ユーザーが入力するのはコメント内容だけ
        fields = ['content']

