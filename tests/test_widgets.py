import pytest
from django import forms
from django.test import override_settings

from unfold_markdown import MarkdownWidget
from unfold_markdown.widgets import get_markdown_setting


class SampleForm(forms.Form):
    content = forms.CharField(widget=MarkdownWidget(), required=True)


def render(widget, name="content", value=None, attrs=None):
    return widget.render(name, value, attrs=attrs)


def test_exported_from_package_root():
    from unfold_markdown import __all__, __version__

    assert "MarkdownWidget" in __all__
    assert __version__


def test_media_lists_easymde_and_config():
    media = str(MarkdownWidget().media)
    assert "unfold_markdown/js/easymde.min.js" in media
    assert "unfold_markdown/js/markdown.config.js" in media
    assert "unfold_markdown/css/easymde.min.css" in media
    assert "unfold_markdown/css/markdown.css" in media


def test_renders_wrapper_and_marker_attribute():
    html = render(MarkdownWidget())
    assert 'class="markdown-widget-wrapper max-w-4xl"' in html
    assert "data-markdown-editor" in html
    assert 'name="content"' in html


def test_passes_through_widget_attrs():
    html = render(MarkdownWidget(), attrs={"id": "id_content", "class": "extra"})
    assert 'id="id_content"' in html
    assert 'class="extra"' in html


def test_empty_value_renders_empty_textarea():
    html = render(MarkdownWidget())
    assert "><" in html.replace("\n", "")
    assert ">None<" not in html


def test_value_is_escaped():
    html = render(MarkdownWidget(), value="<script>x</script>")
    assert "<script>x</script>" not in html
    assert "&lt;script&gt;" in html


def test_round_trips_value_from_form_data():
    form = SampleForm(data={"content": "# Title"})
    assert form.is_valid(), form.errors
    assert form.cleaned_data["content"] == "# Title"


def test_required_attribute_is_suppressed():
    # EasyMDE hides the textarea; a required hidden field blocks browser submit.
    assert "required" not in SampleForm().as_p()


@override_settings(UNFOLD_MARKDOWN={})
def test_no_upload_url_renders_no_data_attribute():
    html = render(MarkdownWidget())
    assert "data-image-upload-url" not in html


@override_settings(UNFOLD_MARKDOWN={"image_upload_url": "/up/"})
def test_upload_url_from_settings():
    assert 'data-image-upload-url="/up/"' in render(MarkdownWidget())


@override_settings(UNFOLD_MARKDOWN={"image_upload_url": "/from-settings/"})
def test_per_widget_upload_url_wins():
    html = render(MarkdownWidget(upload_url="/from-widget/"))
    assert 'data-image-upload-url="/from-widget/"' in html
    assert "/from-settings/" not in html


@override_settings()
def test_missing_setting_falls_back_to_defaults():
    from django.conf import settings

    del settings.UNFOLD_MARKDOWN
    assert get_markdown_setting("image_upload_url") is None
    assert get_markdown_setting("image_upload_dir") == "markdown-images"
    assert get_markdown_setting("image_max_size") == 10 * 1024 * 1024


@pytest.mark.parametrize(
    "key,expected",
    [
        ("image_upload_dir", "markdown-images"),
        ("image_max_size", 10 * 1024 * 1024),
    ],
)
@override_settings(UNFOLD_MARKDOWN={"image_upload_url": "/up/"})
def test_partial_setting_keeps_other_defaults(key, expected):
    assert get_markdown_setting(key) == expected


@override_settings(UNFOLD_MARKDOWN={"image_max_size": 0})
def test_falsy_override_is_respected():
    assert get_markdown_setting("image_max_size") == 0
