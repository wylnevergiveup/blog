from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from BlogApp.models import Post
from .CommentForm import CommentForm
from django.contrib import messages
from django import template

# 添加评论的视图函数
@require_POST
def comment(request, pk):
    # 首先获取文章
    post = get_object_or_404(Post, pk=pk)

    # 封装用户提交的数据，构造表单实例
    form = CommentForm(request.POST)

    #  当调用 form.is_valid() 方法时，django 自动帮我们检查表单的数据是否符合格式要求
    if form.is_valid():
        # 若数据合法就save存储
        # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库
        comment = form.save(commit=False)
        # 关联评论和被评论的文章
        comment.post = post
        comment.save()

        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')

        # redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法
        # 重定向到 get_absolute_url 方法返回的 URL
        return redirect(post)

    else:
        # 检查到数据不合法，我们渲染一个预览页面，用于展示表单的错误。
        # 注意这里被评论的文章 post 也传给了模板，因为我们需要根据 post 来生成表单的提交地址。
        context = {
            'post': post,
            'form': form
        }
        messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
        return render(request, 'CommentsShow/preview.html', context=context)



