from django.urls import path

from .views import IndexView, ItemView

app_name = 'menu'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<slug:slug>/', ItemView.as_view(), name='item')
]
