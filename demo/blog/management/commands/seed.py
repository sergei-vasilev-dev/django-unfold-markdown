from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from blog.models import Article, Section

SAMPLE = """# Hello from django-unfold-markdown

A paragraph with **bold**, *italic* and ~~struck~~ text, plus a [link](https://example.com).

## Checklist

- [x] Toolbar icons render as Material Symbols
- [ ] Preview and side-by-side modes
- [ ] Fullscreen

```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

> Try the image button - with `UNFOLD_MARKDOWN["image_upload_url"]` set it opens
> a file picker instead of asking for a URL.

| Column | Value |
| ------ | ----- |
| One    | 1     |
| Two    | 2     |
"""


class Command(BaseCommand):
    help = "Create the demo superuser (admin/admin) and a sample article."

    def handle(self, *args, **options) -> None:
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            user.set_password("admin")
            user.save()
            self.stdout.write(self.style.SUCCESS("Created superuser admin / admin"))
        else:
            self.stdout.write("Superuser 'admin' already exists")

        article, created = Article.objects.get_or_create(
            title="Sample article",
            defaults={
                "body": SAMPLE,
                "summary": "A short **summary**.",
                "notes": "Notes tab.",
            },
        )
        if created:
            Section.objects.create(
                article=article,
                heading="An inline section",
                content="Editors inside inline formsets initialise too.",
            )
            self.stdout.write(self.style.SUCCESS("Created sample article"))
        else:
            self.stdout.write("Sample article already exists")

        self.stdout.write(
            self.style.SUCCESS(
                "\nOpen http://127.0.0.1:8000/admin/ and log in as admin / admin"
            )
        )
