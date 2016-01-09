# coding: utf-8

from django.views.generic.base import TemplateView
from .models import Article


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context
