from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'url', 'post', 'create_time']
    fields = ['name', 'email', 'url', 'text']

admin.site.register(Comment, CommentAdmin)