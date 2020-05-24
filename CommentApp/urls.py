# 路由函数
from django.conf.urls import url
from . import views

app_name = 'CommentApp'
urlpatterns = [
    url(r'^form/(?P<pk>[0-9]+)/$', views.comment, name='comment'),
]