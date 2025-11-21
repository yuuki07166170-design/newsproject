from django.contrib import admin
from .models import Category, NewsPost, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

# コメント機能：管理画面でコメントを管理できるようにする
class CommentAdmin(admin.ModelAdmin):
    # 一覧表示する項目
    list_display = ('id', 'user', 'news_post', 'content', 'posted_at')
    # クリックして詳細画面に行ける項目
    list_display_links = ('id', 'content')

admin.site.register(Category, CategoryAdmin)
admin.site.register(NewsPost, NewsPostAdmin)
# コメント機能：管理画面に登録
admin.site.register(Comment, CommentAdmin)
