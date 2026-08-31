import pytest
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse

pytestmark = pytest.mark.django_db

URL = "/unfold-markdown/image-upload/"


def test_url_is_reversible():
    assert reverse("unfold_markdown:image_upload") == URL


def test_get_is_not_allowed(client):
    assert client.get(URL).status_code == 405


def test_anonymous_is_forbidden(client, png_upload):
    response = client.post(URL, {"file": png_upload})
    assert response.status_code == 403


def test_non_staff_is_forbidden(client, plain_user, png_upload):
    client.force_login(plain_user)
    response = client.post(URL, {"file": png_upload})
    assert response.status_code == 403


def test_staff_upload_returns_url(client, staff_user, png_upload):
    client.force_login(staff_user)
    response = client.post(URL, {"file": png_upload})
    assert response.status_code == 200
    url = response.json()["url"]
    assert url.startswith("/media/markdown-images/")
    assert url.endswith(".png")


def test_stored_filename_is_randomised(client, staff_user, png_upload):
    client.force_login(staff_user)
    response = client.post(URL, {"file": png_upload})
    url = response.json()["url"]
    assert "shot" not in url
    stored = url.replace("/media/", "")
    assert default_storage.exists(stored)


def test_missing_file_is_rejected(client, staff_user):
    client.force_login(staff_user)
    response = client.post(URL, {})
    assert response.status_code == 400
    assert "error" in response.json()


@pytest.mark.parametrize("name", ["evil.exe", "payload.php", "noextension", "x.svg"])
def test_disallowed_extensions_are_rejected(client, staff_user, name):
    client.force_login(staff_user)
    upload = SimpleUploadedFile(name, b"data", content_type="application/octet-stream")
    response = client.post(URL, {"file": upload})
    assert response.status_code == 400


@override_settings(UNFOLD_MARKDOWN={"image_allowed_extensions": ["svg"]})
def test_allowed_extensions_are_configurable(client, staff_user):
    client.force_login(staff_user)
    upload = SimpleUploadedFile("logo.svg", b"<svg/>", content_type="image/svg+xml")
    assert client.post(URL, {"file": upload}).status_code == 200


def test_extension_check_is_case_insensitive(client, staff_user):
    client.force_login(staff_user)
    upload = SimpleUploadedFile("SHOT.PNG", b"data", content_type="image/png")
    response = client.post(URL, {"file": upload})
    assert response.status_code == 200
    assert response.json()["url"].endswith(".png")


@override_settings(UNFOLD_MARKDOWN={"image_max_size": 10})
def test_oversized_file_is_rejected(client, staff_user):
    client.force_login(staff_user)
    upload = SimpleUploadedFile("big.png", b"x" * 100, content_type="image/png")
    response = client.post(URL, {"file": upload})
    assert response.status_code == 400
    assert "too large" in response.json()["error"].lower()


@override_settings(UNFOLD_MARKDOWN={"image_upload_dir": "custom/dir/"})
def test_upload_dir_is_configurable(client, staff_user, png_upload):
    client.force_login(staff_user)
    response = client.post(URL, {"file": png_upload})
    assert response.json()["url"].startswith("/media/custom/dir/")


def test_csrf_is_enforced(staff_user, png_upload):
    from django.test import Client

    client = Client(enforce_csrf_checks=True)
    client.force_login(staff_user)
    response = client.post(URL, {"file": png_upload})
    assert response.status_code == 403
