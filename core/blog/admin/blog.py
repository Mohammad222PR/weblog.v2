from django.contrib import admin
from blog.models import *


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1
    min_num = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    '''Admin View for Blog'''
    list_display = ('author','title','body','created_time','is_public','updated_time' ,'slug', 'category', 'need_membership')
    list_filter = ('created_time','updated_time','is_public' ,'category','tag')
    search_fields = ('author','title','body'  ,'category')
    ordering = ('created_time','updated_time','is_public' , 'category',)
    prepopulated_fields = {'slug':('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    '''Admin View for Blog'''
    list_display = ('blog','user','title','message','parent','created_time','is_public')
    list_filter = ('created_time','is_public')
    search_fields = ('title','parent','is_public')
    ordering = ('created_time','is_public')
    inlines = [CommentInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''
    list_display = ('title',)
    search_fields = ('title',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    '''Admin View for Tag'''
    list_display = ('title',)
    search_fields = ('title',)