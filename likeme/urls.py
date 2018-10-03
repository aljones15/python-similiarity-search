from django.urls import path

from . import views
app_name = 'likeme'
urlpatterns = [
    path('', views.index, name='index'),
]
