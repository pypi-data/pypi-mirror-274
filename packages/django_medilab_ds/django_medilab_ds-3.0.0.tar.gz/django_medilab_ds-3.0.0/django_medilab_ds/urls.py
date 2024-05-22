from django.urls import path
from . import views
from _data import medilabds

app_name = medilabds.context['template_name']

urlpatterns = [
    # robots.txt는 반드시 가장 먼저
    path('robots.txt', views.robots),
    path('', views.home, name='home'),
]
