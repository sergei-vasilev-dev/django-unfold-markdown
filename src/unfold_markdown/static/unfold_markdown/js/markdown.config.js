// Markdown Editor Configuration for Django Unfold
// Uses EasyMDE with custom styling

(function () {
    'use strict';

    // `data-markdown-editor` is set by the bundled template. The `id^="markdown-"`
    // half keeps editors working for projects still on the pre-0.2 template.
    var MARKDOWN_SELECTOR = 'textarea[data-markdown-editor], textarea[id^="markdown-"]';

    function findTextareas(root) {
        return Array.prototype.slice.call((root || document).querySelectorAll(MARKDOWN_SELECTOR));
    }

    function getCSRFToken() {
        var input = document.querySelector('[name=csrfmiddlewaretoken]');
        if (input && input.value) return input.value;
        var meta = document.querySelector('meta[name="csrf-token"]');
        if (meta) return meta.getAttribute('content') || '';
        var cookie = document.cookie.split('; ').find(function (c) {
            return c.indexOf('csrftoken=') === 0;
        });
        return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
    }

    function createImageUploadAction(uploadUrl) {
        return function uploadImage(editor) {
            var input = document.createElement('input');
            input.type = 'file';
            input.accept = 'image/*';
            input.onchange = function () {
                var file = input.files[0];
                if (!file) return;

                var formData = new FormData();
                formData.append('file', file);

                var cm = editor.codemirror;
                var placeholder = '![Uploading ' + file.name + '…]()';
                var from = cm.getCursor();
                cm.replaceRange(placeholder, from);
                // Track the placeholder through concurrent edits so the URL still
                // lands in the right place if the user keeps typing during upload.
                var marker = cm.markText(from, cm.getCursor(), { className: 'markdown-uploading' });

                fetch(uploadUrl, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': getCSRFToken() },
                    body: formData,
                    credentials: 'same-origin',
                })
                    .then(function (response) {
                        if (!response.ok) {
                            return response.json()
                                .catch(function () { return {}; })
                                .then(function (data) {
                                    throw new Error(data.error || 'HTTP ' + response.status);
                                });
                        }
                        return response.json();
                    })
                    .then(function (data) {
                        if (!data.url) throw new Error('No URL in response');
                        var alt = file.name.replace(/\.[^.]+$/, '');
                        replaceMarker(cm, marker, '![' + alt + '](' + data.url + ')');
                    })
                    .catch(function (err) {
                        replaceMarker(cm, marker, '');
                        window.alert('Image upload failed: ' + err.message);
                    });
            };
            input.click();
        };
    }

    function replaceMarker(cm, marker, text) {
        var range = marker.find();
        marker.clear();
        if (range) {
            cm.replaceRange(text, range.from, range.to);
        } else if (text) {
            cm.replaceRange(text, cm.getCursor());
        }
    }

    var ICON_MAP = {
        'bold': 'format_bold',
        'italic': 'format_italic',
        'strikethrough': 'format_strikethrough',
        'heading-1': 'format_h1',
        'heading-2': 'format_h2',
        'heading-3': 'format_h3',
        'quote': 'format_quote',
        'code': 'code',
        'unordered-list': 'format_list_bulleted',
        'ordered-list': 'format_list_numbered',
        'link': 'link',
        'image': 'image',
        'table': 'table',
        'horizontal-rule': 'horizontal_rule',
        'preview': 'visibility',
        'side-by-side': 'view_sidebar',
        'fullscreen': 'fullscreen',
        'guide': 'help'
    };

    function applyMaterialIcons(textarea, uploadUrl) {
        var toolbar = textarea.parentElement && textarea.parentElement.querySelector('.editor-toolbar');
        if (!toolbar) return;
        Object.keys(ICON_MAP).forEach(function (name) {
            var button = toolbar.querySelector('button.' + name);
            if (!button) return;
            button.innerHTML = '';
            var span = document.createElement('span');
            span.className = 'material-symbols-outlined';
            span.textContent = (name === 'image' && uploadUrl) ? 'upload' : ICON_MAP[name];
            button.appendChild(span);
        });
    }

    function syncTheme(wrapper) {
        if (!wrapper) return;
        wrapper.classList.toggle('dark', document.documentElement.classList.contains('dark'));
    }

    function refreshAll() {
        findTextareas().forEach(function (textarea) {
            if (textarea.easymde && textarea.easymde.codemirror) {
                textarea.easymde.codemirror.refresh();
            }
        });
    }

    function initMarkdownEditor(textarea) {
        if (textarea.easymde) return;
        // Skip the hidden template row Django clones for inline formsets.
        if ((textarea.id || '').indexOf('__prefix__') !== -1) return;
        if (typeof EasyMDE === 'undefined') return;

        var wrapper = textarea.closest('.markdown-widget-wrapper');
        var uploadUrl = wrapper ? wrapper.dataset.imageUploadUrl : null;

        var imageAction = uploadUrl ? createImageUploadAction(uploadUrl) : EasyMDE.drawImage;
        var imageTitle = uploadUrl ? 'Upload Image' : 'Image';

        var easymde = new EasyMDE({
            element: textarea,
            spellChecker: false,
            autosave: {
                enabled: false,
            },
            status: ['lines', 'words', 'cursor'],
            toolbar: [
                {
                    name: "bold",
                    action: EasyMDE.toggleBold,
                    className: "unfold-markdown-button",
                    title: "Bold",
                },
                {
                    name: "italic",
                    action: EasyMDE.toggleItalic,
                    className: "unfold-markdown-button",
                    title: "Italic",
                },
                {
                    name: "strikethrough",
                    action: EasyMDE.toggleStrikethrough,
                    className: "unfold-markdown-button",
                    title: "Strikethrough",
                },
                "|",
                {
                    name: "heading-1",
                    action: EasyMDE.toggleHeading1,
                    className: "unfold-markdown-button",
                    title: "Heading 1",
                },
                {
                    name: "heading-2",
                    action: EasyMDE.toggleHeading2,
                    className: "unfold-markdown-button",
                    title: "Heading 2",
                },
                {
                    name: "heading-3",
                    action: EasyMDE.toggleHeading3,
                    className: "unfold-markdown-button",
                    title: "Heading 3",
                },
                "|",
                {
                    name: "quote",
                    action: EasyMDE.toggleBlockquote,
                    className: "unfold-markdown-button",
                    title: "Quote",
                },
                {
                    name: "code",
                    action: EasyMDE.toggleCodeBlock,
                    className: "unfold-markdown-button",
                    title: "Code",
                },
                {
                    name: "unordered-list",
                    action: EasyMDE.toggleUnorderedList,
                    className: "unfold-markdown-button",
                    title: "Unordered List",
                },
                {
                    name: "ordered-list",
                    action: EasyMDE.toggleOrderedList,
                    className: "unfold-markdown-button",
                    title: "Ordered List",
                },
                "|",
                {
                    name: "link",
                    action: EasyMDE.drawLink,
                    className: "unfold-markdown-button",
                    title: "Link",
                },
                {
                    name: "image",
                    action: imageAction,
                    className: "unfold-markdown-button",
                    title: imageTitle,
                },
                {
                    name: "table",
                    action: EasyMDE.drawTable,
                    className: "unfold-markdown-button",
                    title: "Table",
                },
                {
                    name: "horizontal-rule",
                    action: EasyMDE.drawHorizontalRule,
                    className: "unfold-markdown-button",
                    title: "Horizontal Rule",
                },
                "|",
                {
                    name: "preview",
                    action: EasyMDE.togglePreview,
                    className: "unfold-markdown-button no-disable",
                    title: "Preview",
                },
                {
                    name: "side-by-side",
                    action: EasyMDE.toggleSideBySide,
                    className: "unfold-markdown-button no-disable no-mobile",
                    title: "Side by Side",
                },
                {
                    name: "fullscreen",
                    action: EasyMDE.toggleFullScreen,
                    className: "unfold-markdown-button no-disable no-mobile",
                    title: "Fullscreen",
                },
                "|",
                {
                    name: "guide",
                    action: "https://www.markdownguide.org/basic-syntax/",
                    className: "unfold-markdown-button",
                    title: "Markdown Guide",
                }
            ],
            renderingConfig: {
                codeSyntaxHighlighting: false,
            },
            initialValue: textarea.value,
        });

        textarea.easymde = easymde;

        // Replace FontAwesome icons with Material Symbols once the toolbar is in the DOM.
        setTimeout(function () {
            applyMaterialIcons(textarea, uploadUrl);
        }, 50);

        // CodeMirror measures itself on creation; re-measure after layout settles.
        setTimeout(function () {
            if (easymde.codemirror) easymde.codemirror.refresh();
        }, 100);

        syncTheme(wrapper);
        observeForRefresh(wrapper || textarea, easymde);
    }

    // Tab implementations differ wildly (Unfold uses bare Alpine-bound <a> tags,
    // modeltranslation uses jQuery UI, Django admin uses its own). Rather than
    // matching every markup variant, watch the editor itself: whenever it comes
    // back into view, CodeMirror re-measures. Kept alive for the page's lifetime.
    function observeForRefresh(target, easymde) {
        new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting && easymde.codemirror) {
                    easymde.codemirror.refresh();
                }
            });
        }, { threshold: 0.1 }).observe(target);
    }

    function initAllMarkdownEditors() {
        var pending = findTextareas().filter(function (textarea) {
            return !textarea.easymde && (textarea.id || '').indexOf('__prefix__') === -1;
        });
        if (!pending.length) return;

        // Editors inside an inactive tab have no layout box yet, and CodeMirror
        // renders at zero height if built there. Defer those until they are shown.
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                initMarkdownEditor(entry.target);
                observer.unobserve(entry.target);
            });
        }, { threshold: 0.1 });

        pending.forEach(function (textarea) {
            if (textarea.offsetParent !== null) {
                initMarkdownEditor(textarea);
            } else {
                observer.observe(textarea);
            }
        });
    }

    function ready() {
        // Run after django-modeltranslation's tabbed_translation_fields.js, which
        // also binds on DOMContentLoaded and builds its jQuery UI tabs there.
        setTimeout(initAllMarkdownEditors, 0);

        // Tabs: pick up editors that just became visible, and re-measure the rest.
        document.addEventListener('click', function (event) {
            var target = event.target;
            if (!target || typeof target.closest !== 'function') return;
            var tab = target.closest(
                '[role="tab"], .ui-tabs-anchor, .tab-navigation button, .tabbed-form-tabs button,' +
                // Unfold renders fieldset tabs as plain anchors inside a <nav>.
                '.tab-wrapper, nav a[x-on\\:click], nav a[\\@click]'
            );
            if (!tab) return;
            setTimeout(function () {
                initAllMarkdownEditors();
                refreshAll();
            }, 150);
        });

        var resizeTimeout;
        window.addEventListener('resize', function () {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(refreshAll, 200);
        });

        // Rows added through Django's inline formsets ("Add another").
        document.addEventListener('formset:added', function () {
            setTimeout(initAllMarkdownEditors, 0);
        });

        // Unfold toggles `dark` on <html>.
        new MutationObserver(function () {
            document.querySelectorAll('.markdown-widget-wrapper').forEach(syncTheme);
        }).observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['class'],
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', ready);
    } else {
        ready();
    }

    window.initAllMarkdownEditors = initAllMarkdownEditors;
})();
