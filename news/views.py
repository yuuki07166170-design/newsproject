from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .forms import NewsPostForm, CommentForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import NewsPost, Comment

class IndexView(ListView):
    template_name = "index.html"
    queryset = NewsPost.objects.all().order_by('-posted_at')
    paginate_by = 9


@method_decorator(login_required, name='dispatch')
class CreateNewsView(CreateView):
    form_class = NewsPostForm
    template_name = "post_news.html"
    success_url = reverse_lazy('news:post_done')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    template_name = "post_success.html"

class CategoryView(ListView):
    template_name = "index.html"
    paginate_by = 9

    def get_queryset(self):
        category_id = self.kwargs['category']
        categories = NewsPost.objects.filter(category=category_id).order_by('-posted_at')
        return categories
    
class UserView(ListView):
    template_name = "index.html"
    paginate_by = 9

    def get_queryset(self):
        user_id = self.kwargs['user']
        user_posts = NewsPost.objects.filter(user=user_id).order_by('-posted_at')
        return user_posts
    
class DetailView(DetailView):
    template_name = "detail.html"
    model = NewsPost

    def get_context_data(self, **kwargs):
        # 親クラスのメソッドを呼び出してコンテキストを取得
        context = super().get_context_data(**kwargs)
        # コメント投稿フォームを追加
        context['comment_form'] = CommentForm()
        # このニュースに紐づくコメント一覧を追加
        context['comments'] = self.object.comments.all()
        return context

@method_decorator(login_required, name='dispatch')
class CommentCreateView(CreateView):
    form_class = CommentForm
    model = Comment

    def form_valid(self, form):
        # フォームのデータを保存せずにインスタンスを取得
        comment = form.save(commit=False)
        # URLパラメータからニュース投稿IDを設定
        comment.news_post_id = self.kwargs['pk']
        # コメントにログインユーザーを設定
        comment.user = self.request.user
        # データベースに保存
        comment.save()
        # ニュース詳細ページにリダイレクト
        return redirect('news:news_detail', pk=self.kwargs['pk'])

class MypageView(ListView):
    template_name = "mypage.html"
    paginate_by = 9

    def get_queryset(self):
        queryset = NewsPost.objects.filter(user=self.request.user).order_by('-posted_at')
        return queryset
    
class NewsDeleteView(DeleteView):
    model = NewsPost
    template_name = "news_delete.html"
    success_url = reverse_lazy('news:mypage')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        # 削除後に戻るニュース詳細ページのURLを生成
        return reverse_lazy('news:news_detail', kwargs={'pk': self.object.news_post.pk})
    
    def delete(self, request, *args, **kwargs):
        # 削除対象のコメントを取得
        comment = self.get_object()
        # コメントの投稿者とログインユーザーが一致するか確認
        if comment.user == request.user:
            # 一致する場合は削除を実行
            return super().delete(request, *args, **kwargs)
        # 一致しない場合はニュース詳細ページにリダイレクト
        return redirect('news:news_detail', pk=comment.news_post.pk)