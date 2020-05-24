from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# 分类数据表
class Category(models.Model):
    """
    django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)
    """在创建完对象之后 会自动调用, 它完成对象的初始化的功能"""

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 标签数据表
class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 文章数据表
class Post(models.Model):
    # 文章标题
    title = models.CharField('标题', max_length=70)

    # 文章正文，大段文本使用TextField
    body = models.TextField('正文')

    # 创建时间，存储时间字段用DataTimeField
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    # 最后一次修改时间，存储时间字段用DataTimeField
    modified_time = models.DateTimeField('修改时间', default=timezone.now)

    # 重写save方法
    def save(self, *args, **kwargs):
        # save的时候自动更新modified_time字段
        self.modified_time = timezone.now()

        # 自动拉去摘要
        # 摘要也要进行渲染，所以实例化一个md对象
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.fenced_code',
        ])
        # 首先先渲染成html页面
        # strip_tags去掉html所有的标签
        self.excerpt = strip_tags(md.convert(self.body))[:10]

        super().save(*args, **kwargs)

    # 摘要
    excerpt = models.CharField('摘要', max_length=200, blank=True)

    """
    这是分类与标签，分类与标签的模型我们已经定义在上面
    我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来
    我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一
    对多的关联关系。且自 django 2.0 以后，ForeignKey 必须传入一个 on_delete 参数用来指定当关联的
    数据被删除时，被关联的数据的行为，我们这里假定当某个分类被删除时，该分类下全部文章也同时被删除，因此     # 使用 models.CASCADE 参数，意为级联删除。
    而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用
    ManyToManyField，表明这是多对多的关联关系。
    同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    https://docs.djangoproject.com/en/2.2/topics/db/models/#relationships
    """
    # 设置主键(category)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    # 关联Tag数据表
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    """
    文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    django.contrib.auth 是 django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 
    django 为我们已经写好的用户模型。
    这里我们通过 ForeignKey 把文章和 User 关联了起来。
    因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和Category 类似。
    """
    # 作者名称
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # 参数1：在BlogApp应用下的details函数
        # reverse 函数会去解析这个视图函数对应的 URL，这里 detail 对应的规则就是 posts/<int:pk>/ int 部分会被后面传入的参数 pk 替换
        return reverse('BlogApp:details', kwargs={'pk':self.pk})
