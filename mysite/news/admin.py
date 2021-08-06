from django import forms
from django.contrib import admin
from news.models import News, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title', 'created_at', 'is_published', 'category')
    list_display_links = ('title', 'id')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title', 'id')
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category)
