from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('index-fbv', views.index_fbv, name='index-fbv'),
    path('index-cbv', views.IndexView.as_view(),name='index-cbv'),
]