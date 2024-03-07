"""TogedaBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="2geda API",
        default_version="v2",
        description="2geda REST API",
        terms_of_service="https://2geda.net",
        contact=openapi.Contact(email="info@2geda.net"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_routes = [
    path("user/", include("user.urls", namespace="user")),
    path("business/", include("business.urls", namespace="business")),
    path("education/", include("education.urls", namespace="education")),
    path("polls/", include("poll.urls", namespace="poll")),
    path("stereo/", include("stereo.urls", namespace="stereo")),
    path("feeds/", include("feeds.urls", namespace="feeds")),
    # path("commerce/", include("commerce.urls")),
    # path("ticket/", include("ticket.urls")),
    # path("chat/", include("chat.urls")),
    # path("reward/", include(reward_url)),
    # path("utils/", include(utils_url)),
    # path("fund-account", MakePaymentView.as_view()),
    # path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_routes)),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if not settings.USE_S3:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
