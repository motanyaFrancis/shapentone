from django.contrib import admin
from .models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created', 'date_modified', 'published']
    list_filter = ['date_created', 'date_modified', 'published']
    search_fields = ['title', ]
    list_editable = ['published',]

# Register your models here.
admin.site.register(PostCategory)
admin.site.register(Article, ArticleAdmin)
