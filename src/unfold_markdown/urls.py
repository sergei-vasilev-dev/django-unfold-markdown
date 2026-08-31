from django.urls import path

from . import views

app_name = "unfold_markdown"

urlpatterns = [
    path("image-upload/", views.image_upload, name="image_upload"),
]
