from django.views.generic import TemplateView, CreateView, ListView
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.models import Article


class ArticleFeed(LoginRequiredMixin, TemplateView):
    template_name = "core/feed.html"
    title = "Feed"
    login_url = 'account:admin_login'

    def get_context_data(self, **kwargs):
        context = super(ArticleFeed, self).get_context_data(**kwargs)
        articles = Article.objects.all()
        if articles.count() > 0:
            paginator = Paginator(articles, 20)
            page = self.request.GET.get('articlespage')
            try:
                final_articles = paginator.page(page) #
            except PageNotAnInteger:
                final_articles = paginator.page(1)
            except EmptyPage:
                final_articles = paginator.page(paginator.num_pages)
            context['articles'] = final_articles
        return context