import posixpath
import uuid

from django.core.files.storage import default_storage
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from .widgets import get_markdown_setting


@require_POST
@csrf_protect
def image_upload(request: HttpRequest) -> JsonResponse:
    """Store an uploaded image and return its URL as ``{"url": ...}``."""
    user = getattr(request, "user", None)
    if user is None or not user.is_authenticated or not user.is_staff:
        return JsonResponse({"error": "Forbidden"}, status=403)

    file = request.FILES.get("file")
    if not file:
        return JsonResponse({"error": "No file provided"}, status=400)

    allowed = {
        ext.lower().lstrip(".")
        for ext in get_markdown_setting("image_allowed_extensions")
    }
    _, _, ext = file.name.rpartition(".")
    ext = ext.lower()
    if not ext or ext not in allowed:
        return JsonResponse(
            {"error": f"File type not allowed. Allowed: {', '.join(sorted(allowed))}"},
            status=400,
        )

    max_size = get_markdown_setting("image_max_size")
    if file.size > max_size:
        return JsonResponse(
            {"error": f"File too large. Maximum size: {max_size // (1024 * 1024)}MB"},
            status=400,
        )

    upload_dir = str(get_markdown_setting("image_upload_dir")).strip("/")
    name = posixpath.join(upload_dir, f"{uuid.uuid4().hex}.{ext}")
    path = default_storage.save(name, file)

    return JsonResponse({"url": default_storage.url(path)})
