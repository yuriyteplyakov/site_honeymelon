from django.contrib import admin
from blog.models import Post, Comment, Review
# Register your models here.


@admin.register(Post)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_created', 'date_updated']
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'date_created', 'name_author']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['image',]