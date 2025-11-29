from typing import Any, Optional

from django.forms import Widget


class MarkdownWidget(Widget):
    template_name = "unfold_markdown/markdown.html"

    class Media:
        css = {
            "all": (
                "unfold_markdown/css/easymde.min.css",
                "unfold_markdown/css/markdown.css",
            )
        }
        js = (
            "unfold_markdown/js/easymde.min.js",
            "unfold_markdown/js/markdown.config.js",
        )

    def __init__(self, attrs: Optional[dict[str, Any]] = None) -> None:
        super().__init__(attrs)

