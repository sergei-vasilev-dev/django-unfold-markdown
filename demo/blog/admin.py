from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, StackedInline

from unfold_markdown import MarkdownWidget

from .models import Article, Section


class SectionInline(StackedInline):
    model = Section
    extra = 0
    formfield_overrides = {models.TextField: {"widget": MarkdownWidget}}


@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    list_display = ("title",)
    inlines = (SectionInline,)
    formfield_overrides = {models.TextField: {"widget": MarkdownWidget}}
    fieldsets = (
        (None, {"fields": ("title", "body")}),
        # Unfold renders "tab" fieldsets hidden behind Alpine's x-show. Editors
        # built in a hidden container come out zero-height, which is what the
        # lazy IntersectionObserver init in markdown.config.js is there to fix.
        ("Summary", {"classes": ("tab",), "fields": ("summary",)}),
        ("Notes", {"classes": ("tab",), "fields": ("notes",)}),
    )
