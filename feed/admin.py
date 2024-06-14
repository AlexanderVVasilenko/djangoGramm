from django.contrib import admin

from feed.models import Post, Comment, Photo, Like


class PhotoInline(admin.StackedInline):
    model = Photo


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', "created", "id")
    list_filter = ('user', "created")
    search_fields = ('user__username',)
    date_hierarchy = 'created'
    ordering = ('-created',)
    inlines = [
        PhotoInline
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', "post")
    list_filter = ('created',)
    search_fields = ('user',)
    readonly_fields = ('content',)
    date_hierarchy = 'created'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)
