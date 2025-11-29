# Django Unfold Markdown Widget

Markdown editor widget for [Django Unfold](https://github.com/unfoldadmin/django-unfold) admin using [EasyMDE](https://github.com/Ionaru/easy-markdown-editor).

## Features

- **Plain text editor** with monospace font
- **Side-by-side preview** and fullscreen modes
- **Dark/light theme** integration with Unfold
- **Material Symbols icons** matching Unfold design
- **Toolbar**: bold, italic, strikethrough, headings, lists, links, images, tables, horizontal rules
- **No autosave** (saves on form submit)
- **Responsive** design

## Installation

```bash
pip install django-unfold-markdown
```

## Configuration

Add to your `INSTALLED_APPS`:

```python
# settings.py
INSTALLED_APPS = [
    "unfold",
    "unfold_markdown",  # Add this
    # ...
]
```

## Usage

### For all TextField fields

```python
# admin.py
from django.db import models
from unfold.admin import ModelAdmin
from unfold_markdown.widgets import MarkdownWidget

@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    formfield_overrides = {
        models.TextField: {"widget": MarkdownWidget}
    }
```

### For specific fields

```python
from django import forms
from unfold_markdown.widgets import MarkdownWidget

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=MarkdownWidget())
    
    class Meta:
        model = Article
        fields = '__all__'

@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    form = ArticleForm
```

## Storage and Rendering

The widget stores pure Markdown text in your database. To render Markdown as HTML, use a Python library:

```python
# Using markdown
from markdown import markdown
html = markdown(article.content)

# Using mistune
import mistune
html = mistune.html(article.content)
```

## Requirements

- Python ≥ 3.10
- Django ≥ 4.2
- django-unfold ≥ 0.70.0

## License

MIT License

## Credits

- **EasyMDE**: [Ionaru/easy-markdown-editor](https://github.com/Ionaru/easy-markdown-editor) (MIT License)
- **Django Unfold**: [unfoldadmin/django-unfold](https://github.com/unfoldadmin/django-unfold) (MIT License)

