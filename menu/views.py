from django.views.generic import ListView, DetailView

from .models import MenuItem


class IndexView(ListView):
    model = MenuItem
    template_name = 'menu/index.html'


class ItemView(DetailView):
    model = MenuItem
    template_name = 'menu/detail.html'
