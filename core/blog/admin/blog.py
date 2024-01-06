from django.contrib import admin
from blog.models import *


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    '''Admin View for Blog'''
    list_display = ('author','title','body','created_time','is_public','updated_time' ,'slug', 'category','is_membership')
    list_filter = ('created_time','updated_time','is_public' ,'category','tag','is_membership')
    search_fields = ('author','title','body'  ,'category')
    ordering = ('created_time','updated_time','is_public' , 'category',)
    prepopulated_fields = {'slug':('title',)}