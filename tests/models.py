from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    class Meta:
        app_label = "tests"

    def __str__(self) -> str:
        return self.title
