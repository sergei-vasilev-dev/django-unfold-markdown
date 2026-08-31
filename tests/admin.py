from django.contrib import admin
from unfold.admin import ModelAdmin

from unfold_markdown import MarkdownWidget

from .models import Article


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    formfield_overrides = {
        Article._meta.get_field("content").__class__: {"widget": MarkdownWidget},
    }
