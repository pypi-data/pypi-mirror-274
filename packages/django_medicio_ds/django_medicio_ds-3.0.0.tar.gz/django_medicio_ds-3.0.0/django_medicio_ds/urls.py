from django.urls import path
from . import views
from _data import mediciods


app_name = mediciods.context['template_name']

urlpatterns = [
    # robots.txt는 반드시 가장 먼저
    path('robots.txt', views.robots),
    path('', views.home, name='home'),
]
