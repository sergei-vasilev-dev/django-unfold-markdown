from typing import Any

from django.conf import settings
from django.forms import Widget

DEFAULTS: dict[str, Any] = {
    "image_upload_url": None,
    "image_upload_dir": "markdown-images",
    "image_max_size": 10 * 1024 * 1024,
    "image_allowed_extensions": (
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp",
        "bmp",
        "ico",
        "avif",
    ),
}


def get_markdown_setting(key: str, default: Any = None) -> Any:
    """Read a key from the ``UNFOLD_MARKDOWN`` setting dict."""
    config = getattr(settings, "UNFOLD_MARKDOWN", None) or {}
    if key in config:
        return config[key]
    if default is not None:
        return default
    return DEFAULTS.get(key)


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

    def __init__(
        self,
        attrs: dict[str, Any] | None = None,
        upload_url: str | None = None,
    ) -> None:
        super().__init__(attrs)
        self.upload_url = upload_url

    def use_required_attribute(self, initial: Any) -> bool:
        # EasyMDE hides the underlying <textarea>. A hidden field carrying
        # ``required`` makes browsers abort submit with "not focusable".
        return False

    def get_context(self, name: str, value: Any, attrs: Any) -> dict[str, Any]:
        context = super().get_context(name, value, attrs)
        upload_url = self.upload_url or get_markdown_setting("image_upload_url")
        context["image_upload_url"] = upload_url
        return context
