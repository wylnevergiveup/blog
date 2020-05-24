#  django 需要知道当用户访问不同的网址时，
#  应该如何处理这些不同的网址（即所说的路由）。django 的做法是把不同的网址对应的处理函数写在一个 urls.py 文件里，
#  当用户访问某个网址时，django 就去会这个文件里找，如果找到这个网址，就会调用和它绑定在一起的处理函数

from django.conf.urls import url
# 新版：from django.urls import url
from . import views

app_name = 'BlogApp'
urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.details, name='details'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^categories/(?P<pk>[0-9]+)/$', views.category, name='category'),
    url(r'^tags/(?P<pk>[0-9]+)/$', views.tag, name='tag' ),
    url(r'index', views.index, name='index'),
    url(r'full-width', views.index, name='index'),
    url(r'about.html', views.index, name='index'),
    url(r'contact.html', views.index, name='index'),
]