from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
    path("subscriptions/", include("subscriptions.urls")),
    path("tinymce/", include("tinymce.urls")),
    path("", include("pwa.urls")),
    path("", include("base.urls")),
    path("", include("authentication.urls")),
    path("", include("dashboard.urls")),
    path("", include("myRequest.urls")),
    path("", include("payment.urls")),
    path("", include("articles.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
