import shutil

import pytest
from django.conf import settings


@pytest.fixture(autouse=True)
def _clean_media():
    yield
    shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)


@pytest.fixture
def staff_user(django_user_model):
    return django_user_model.objects.create_user(
        username="staffer", password="pw", is_staff=True
    )


@pytest.fixture
def plain_user(django_user_model):
    return django_user_model.objects.create_user(username="plain", password="pw")


@pytest.fixture
def png_upload():
    from django.core.files.uploadedfile import SimpleUploadedFile

    # 1x1 transparent PNG
    data = bytes.fromhex(
        "89504e470d0a1a0a0000000d494844520000000100000001080600000"
        "01f15c4890000000a49444154789c6300010000050001"
        "0d0a2db40000000049454e44ae426082"
    )
    return SimpleUploadedFile("shot.png", data, content_type="image/png")
