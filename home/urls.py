from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='coursework-login'),
    path('index/', views.index, name='coursework-home'),
]
