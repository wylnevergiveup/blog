# 评论的数据路模型
from django.db import models
from django.utils import timezone

# 评论(数据库都要继承models.Model类，里面元素调用model对象)
class Comment(models.Model):
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮件')
    url = models.URLField('网址', blank=True)  # url可为空
    text = models.TextField('内容')
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    # 一对多关联
    post = models.ForeignKey('BlogApp.Post', verbose_name='文章', on_delete=models.CASCADE)

    # 定义模型显示名字
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        # 内部类Meta能够指定能够指定一些属性的值来规定该模型具有的一些特性
        # ordering属性用来指定文章排序方式
        ordering = ['-create_time']

    def __str__(self):
        return '{}:{}'.format(self.name, self.text[:20])