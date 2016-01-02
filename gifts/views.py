from django.http import HttpResponse
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
