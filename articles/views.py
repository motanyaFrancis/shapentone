from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View

from articles.models import *

# Create your views here.


class ArticleView(ListView):
    template_name = 'articles.html'
    queryset = Article.objects.all().order_by(
        '-date_created').filter(published=True)
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        context['latest_article'] = Article.objects.order_by('-date_created').filter(published=True)[:1]

        return context


def article(request):
    return render(request, 'articles.html')


def article_details(request):
    return render(request, 'article-details.html')


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article-details.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):

        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.order_by('-date_created').filter(published=True)[:5]
        return context
