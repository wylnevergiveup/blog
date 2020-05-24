# 该文件用于存放自定义的模板标签的代码

# 自定义模板标签的原理类似于构造一个接口，能够让前端获取数据库中的文章列表Post_list
from django import template
from ..models import Post, Category, Tag

# 实例化一个template对象
register = template.Library()

# 最新文章模板标签
@register.inclusion_tag('BlogShow/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-create_time')[:num],
    }

# 归档模板标签
@register.inclusion_tag('BlogShow/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    return {
        'date_list': Post.objects.dates('create_time', 'month', order='DESC'),
    }

# 归档模板标签
@register.inclusion_tag('BlogShow/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    return {
        'category_list': Category.objects.all(),
    }

# 标签云模板标签
@register.inclusion_tag('BlogShow/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    return {
        'tag_list': Tag.objects.all(),
    }
