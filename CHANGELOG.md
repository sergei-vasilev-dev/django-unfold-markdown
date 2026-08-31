# Changelog

All notable changes to this project are documented here. This project adheres to
[Semantic Versioning](https://semver.org/).

## [0.2.1] - 2026-08-31

### Fixed

- **Preview mode covered the whole admin page with a blank white sheet**
  ([#1](https://github.com/sergei-vasilev-dev/django-unfold-markdown/issues/1)).
  EasyMDE puts the class `editor-preview-full` on the *ordinary inline preview*
  as well as the fullscreen one. `markdown.css` styled that class, unscoped, as
  a fixed full-viewport overlay — intended for fullscreen — so clicking Preview
  blanked out the page. The overlay is now scoped to `.CodeMirror-fullscreen`;
  outside fullscreen EasyMDE's own absolute positioning correctly fills the
  editor box. Fullscreen and side-by-side are unchanged.

### Changed

- **No more third-party CDN request.** EasyMDE injected a stylesheet link to
  `maxcdn.bootstrapcdn.com` on every page carrying the widget. Every icon is
  replaced with a Material Symbol and `i.fa` is hidden, so the download bought
  nothing while leaking referrer data and breaking offline or air-gapped
  deployments. Disabled via `autoDownloadFontAwesome: false`.

## [0.2.0] - 2026-08-31

Thanks to [@GaspardMerten](https://github.com/GaspardMerten), whose
[fork](https://github.com/GaspardMerten/django-unfold-markdown) is the origin of
the image upload feature and the hidden-tab initialisation fix.

### Added

- **Image upload.** With `UNFOLD_MARKDOWN["image_upload_url"]` set, the toolbar's
  image button opens a file picker instead of prompting for a URL. Ships a
  staff-only, CSRF-protected upload view at `unfold_markdown.urls`, configurable
  through `image_upload_dir`, `image_max_size` and `image_allowed_extensions`.
  A per-widget `MarkdownWidget(upload_url=...)` overrides the setting.
- Test suite (40 tests) covering the widget, the upload view, admin integration
  and the bundled assets.
- `demo/` — a runnable Django project for manual testing. See the README.
- Continuous integration across Python 3.10–3.13 and Django 4.2–6.1.

### Fixed

- **Editors inside hidden tabs rendered zero-height.** CodeMirror cannot measure
  itself inside a `display: none` container, which broke Unfold fieldset tabs and
  django-modeltranslation's tabbed fields. Editors now initialise lazily when
  they first become visible, and re-measure whenever they are shown again.
- **Editors in inline formsets.** Rows added with "Add another" now get an
  editor, and the hidden `__prefix__` template row is no longer consumed by
  EasyMDE — which previously broke the Add button after the first use.
- **The widget ignored its `attrs`.** The template hardcoded
  `id="markdown-<name>"` and dropped everything passed in, so admin labels did
  not point at the field. Attributes now render, and editors are located by
  `data-markdown-editor` instead of an id prefix.
- **`required` blocked form submission.** EasyMDE hides the underlying
  `<textarea>`, and browsers refuse to submit a form with a required field they
  cannot focus. The widget no longer emits `required`.
- The dark class is now applied when the page loads in dark mode, not only when
  the theme is toggled afterwards.

### Changed

- **EasyMDE 2.18.0 → 2.21.0.** No CSS class or toolbar API changes.
- **django-unfold**: minimum raised to 0.99 on Python 3.12+, where it is
  installable. Python 3.10/3.11 keep the 0.70 floor rather than failing to
  resolve. Verified against 0.104.1 on Django 6.1 and 0.81.0 on Django 5.2.
- Packaging moved from Poetry's legacy layout to PEP 621 with hatchling.
  `MANIFEST.in` is gone; the built wheel is unchanged in content.
- Dev tooling: pytest 9.1, pytest-django 4.14, ruff 0.16.5.

### Compatibility

Drop-in for 0.1.x. Projects that overrode
`unfold_markdown/templates/unfold_markdown/markdown.html` keep working — the
`textarea[id^="markdown-"]` selector is retained as a fallback — but should add
`data-markdown-editor` to the textarea, as the fallback will be removed in 0.3.

## [0.1.2] - 2025-11-30

- Tab initialisation fix and dark theme support.
