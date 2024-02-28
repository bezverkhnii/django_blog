from django.contrib import admin
from .models import Author, Tag, Post, Comment
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")

class TagAdmin(admin.ModelAdmin):
    list_display = ("caption",)

class PostAdmin(admin.ModelAdmin):
    list_filter = ("date", "tag", "author")
    list_display = ("title", "date","author")
    prepopulated_fields = {"slug" : ("title", )}


class CommentAdmin(admin.ModelAdmin):
    list_filter = ("id",)
    list_display = ("username", "text")

admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)