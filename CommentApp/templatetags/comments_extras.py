# 自定义模板标签，就是自己写模板标签的对应的功能
from django import template
from ..CommentForm import CommentForm

# 实例化一个模板标签对象
register = template.Library()

# 接收参数：post实例和CommentForm对应的form实例
@register.inclusion_tag('CommentsShow/inclusions/_form.html', takes_context=True)
def show_comments_form(context, post, form=None):
    if form is None:
        form = CommentForm()
    return {
        'form': form,
        'post': post,
    }

# 评论展示
@register.inclusion_tag('CommentsShow/inclusions/_list.html', takes_context=True)
def show_comment(context, post):
    # 通过post.comment_set.all()的方式获取post对应的全部评论
    # 这里的comment_set等价于Comment.objects.filter(post=post), 即根据 post 来过滤该 post 下的全部评论
    # 既然我们已经有了一个 Post 模型的实例 post（它对应的是 Post 在数据库中的一条记录），那么获取和 post 关联的评论列表有一个简单方法，即调用它的 xxx_set 属性来获取一个类似于 objects 的模型管理器
    comment_list = post.comment_set.all().order_by('-create_time')
    comment_count = comment_list.count()
    return {
        'comment_count': comment_count,
        'comment_list': comment_list,
    }