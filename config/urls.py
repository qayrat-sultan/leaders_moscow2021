from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from demo.views import MyFilesView

urlpatterns = [
    path("file/", include("demo.urls")),
    path("admin/", admin.site.urls),
    path("", MyFilesView.as_view(template_name="files.html"))
    # Your stuff: custom urls includes go here
] + static("files/", document_root="bluring_zip_files") + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
