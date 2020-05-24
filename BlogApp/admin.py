from django.contrib import admin
from .models import Post, Category, Tag

class PostAdmin(admin.ModelAdmin):
    # 细化文章列表
    list_display = ['title', 'body', 'create_time', 'modified_time', 'excerpt', 'category', 'author']
    # 简化新增的表单
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        # 以将 request.user 关联到创建的 Post 实例
        obj.author = request.user
        super().save_model(request, obj, form, change)


# 在后台注册我们自己创建的几个模型
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
