from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    summary = models.TextField(blank=True, help_text="Markdown, rendered in a tab.")
    body = models.TextField(blank=True)
    notes = models.TextField(blank=True, help_text="Lives in a second Unfold tab.")

    def __str__(self) -> str:
        return self.title


class Section(models.Model):
    """Exists to exercise the widget inside a Django inline formset."""

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="sections"
    )
    heading = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.heading
