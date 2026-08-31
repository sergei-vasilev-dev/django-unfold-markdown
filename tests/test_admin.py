import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_client_(client, django_user_model):
    user = django_user_model.objects.create_superuser(
        username="root", email="root@example.com", password="pw"
    )
    client.force_login(user)
    return client


def test_add_form_renders_the_editor(admin_client_):
    response = admin_client_.get("/admin/tests/article/add/")
    assert response.status_code == 200
    html = response.content.decode()
    assert "markdown-widget-wrapper" in html
    assert "data-markdown-editor" in html
    assert 'data-image-upload-url="/unfold-markdown/image-upload/"' in html


def test_add_form_includes_widget_media(admin_client_):
    html = admin_client_.get("/admin/tests/article/add/").content.decode()
    assert "unfold_markdown/js/easymde.min.js" in html
    assert "unfold_markdown/js/markdown.config.js" in html
    assert "unfold_markdown/css/markdown.css" in html


def test_change_form_shows_stored_markdown(admin_client_):
    from tests.models import Article

    article = Article.objects.create(title="T", content="# Heading\n\nBody")
    html = admin_client_.get(
        f"/admin/tests/article/{article.pk}/change/"
    ).content.decode()
    assert "# Heading" in html


def test_saving_persists_markdown(admin_client_):
    from tests.models import Article

    response = admin_client_.post(
        "/admin/tests/article/add/",
        {"title": "T", "content": "**bold**", "_save": ""},
    )
    assert response.status_code == 302
    assert Article.objects.get(title="T").content == "**bold**"
