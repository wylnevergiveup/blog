"""MyBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('BlogApp.urls')),
    url(r'', include('CommentApp.urls')),
]

# 我们前面建立了一个 urls.py 文件，并且绑定了 URL 和视图函数 index，但是 django 并不知道。django 匹配 URL 模式是在 blogproject 目录（即 settings.py 文件所在的目录）的 urls.py 下的，所以我们要把 blog 应用下的 urls.py 文件包含到 blogproject\urls.py 里去
# include 前还有一个 ''，这是一个空字符串。这里也可以写其它字符串，django 会把这个字符串和后面 include 的 urls.py 文件中的 URL 拼接
