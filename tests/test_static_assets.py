from pathlib import Path

import unfold_markdown

ROOT = Path(unfold_markdown.__file__).parent
STATIC = ROOT / "static" / "unfold_markdown"

EXPECTED_EASYMDE_VERSION = "2.21.0"


def test_bundled_assets_are_present():
    for rel in [
        "js/easymde.min.js",
        "js/markdown.config.js",
        "js/LICENSE",
        "css/easymde.min.css",
        "css/markdown.css",
    ]:
        assert (STATIC / rel).is_file(), rel


def test_template_ships_with_the_package():
    assert (ROOT / "templates" / "unfold_markdown" / "markdown.html").is_file()


def test_bundled_easymde_version_matches_expected():
    for rel in ["js/easymde.min.js", "css/easymde.min.css"]:
        header = (STATIC / rel).read_text(errors="ignore")[:200]
        assert f"easymde v{EXPECTED_EASYMDE_VERSION}" in header, rel


def test_config_selects_by_data_attribute():
    js = (STATIC / "js" / "markdown.config.js").read_text()
    assert "textarea[data-markdown-editor]" in js
    # Legacy fallback for projects on an overridden pre-0.2 template.
    assert 'textarea[id^="markdown-"]' in js


def test_config_has_no_third_party_urls():
    js = (STATIC / "js" / "markdown.config.js").read_text()
    for line in js.splitlines():
        if "http" in line and "markdownguide.org" not in line:
            assert line.strip().startswith("//"), line


def _markdown_css() -> str:
    return (STATIC / "css" / "markdown.css").read_text()


def test_fullscreen_preview_overlay_stays_scoped():
    """Regression for #1: preview covered the whole page.

    EasyMDE puts `editor-preview-full` on the ordinary inline preview too, not
    only the fullscreen one. An unscoped `.editor-preview-full { position:
    fixed; inset: 50px 0 0 0 }` therefore turns a plain Preview click into a
    full-viewport white sheet over the admin. Every rule targeting that class
    must be qualified with .CodeMirror-fullscreen.
    """
    for line in _markdown_css().splitlines():
        stripped = line.strip()
        if "editor-preview-full" not in stripped or stripped.startswith("*"):
            continue
        if not stripped.endswith("{") and "," not in stripped:
            continue
        assert ".CodeMirror-fullscreen" in stripped, (
            f"unscoped editor-preview-full selector would cover the page: {stripped}"
        )


def test_inline_preview_typography_is_styled():
    """The inline preview carries both `editor-preview` and `editor-preview-full`,
    so the prose rules keyed on `.editor-preview` reach it."""
    css = _markdown_css()
    for selector in [
        ".markdown-widget-wrapper .editor-preview h1",
        ".markdown-widget-wrapper .editor-preview table",
        ".markdown-widget-wrapper .editor-preview blockquote",
    ]:
        assert selector in css, selector


def test_fontawesome_cdn_download_is_disabled():
    """EasyMDE injects a <link> to maxcdn.bootstrapcdn.com unless told not to.
    Every icon is swapped for a Material Symbol, so that request buys nothing
    and makes the admin depend on a third-party host."""
    js = (STATIC / "js" / "markdown.config.js").read_text()
    assert "autoDownloadFontAwesome: false" in js
