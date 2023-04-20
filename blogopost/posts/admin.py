from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group', 'image')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    list_editable = ('group', 'image')
    raw_id_fields = ('author',)
    date_hierarchy = 'pub_date'
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('author__username',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    raw_id_fields = ('author',)
    date_hierarchy = 'pub_date'
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Group)
