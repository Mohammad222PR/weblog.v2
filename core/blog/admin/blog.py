from django.contrib import admin
from blog.models import *


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    '''Admin View for Blog'''
    list_display = ('author','title','body','created_time','updated_time' ,'slug', 'category')
    list_filter = ('created_time','updated_time', 'category','tag')
    readonly_fields = ('author','title','body','created_time','updated_time' ,'slug', 'category',)
    search_fields = ('author','title','body' ,'slug', 'category')
    ordering = ('created_time','updated_time' , 'category',)
    prepopulated_fields = {'slug':('title',)}