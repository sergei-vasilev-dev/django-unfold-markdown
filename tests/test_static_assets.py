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
