from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
import markdown
import re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

# 接受了一个名为 request 的参数，这个 request 就是 django 为我们封装好的 HTTP 请求
# def index(request):
#     return render(request, 'BlogShow/index.html', context={
#         'title': '何达女装评到频道',
#         'welcome': '欢迎来到何达女装频道'
#     })
# # HTML 模板中的内容字符串被传递给 HttpResponse 对象并返回给浏览器

def index(request):
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'BlogShow/index.html', context={'post_list': post_list})

def details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 把post的body文本转化为html文本,  extensions是对 Markdown 语法的拓展
    # 实例化了一个 markdown.Markdown 对象 md
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.fenced_code',
        # TocExtension函数用于处理标题的锚点值,这里的TocExtension是一个函数，类似于原本写死，现在能够传参转化了
        TocExtension(slugify=slugify)
    ])
    # 传参
    post.body = md.convert(post.body)
    # post.body没有toc属性和值，所以把md的赋值给post
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'BlogShow/detail.html', context={'post': post})

# 归档视图，显示某个时间段内的所有文章
def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year = year,
                                    create_time__month = month
                                    ).order_by('-create_time')
    return render(request, 'BlogShow/index.html', context={'post_list':post_list})

# 分类视图，显示某个分类的所有文章
def category(request, pk):
    # 首先检索Category数据库中序号为pk分类标签
    result_category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=result_category).order_by('-create_time')
    return render(request, 'BlogShow/index.html', context={'post_list': post_list})

# 标签视图，显示某个标签的所有文章
def tag(request, pk):
    tag_result = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag_result).order_by('-create_time')
    return render(request, 'BlogShow/index.html', context={'post_list': post_list})