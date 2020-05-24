# 评论表单，django 的表单类必须继承自 forms.Form 类或者 forms.ModelForm 类
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        # 对应的数据库模型是 Comment
        model = Comment
        # 指定表单展示的字段
        fields = ['name', 'email', 'text']
