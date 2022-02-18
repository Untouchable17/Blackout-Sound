from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Audio library",
        default_version='v1',
        description="Небольшая аналогия SoundCloud на Django/Rest Framework",
        contact=openapi.Contact(url="https://www.youtube.com/channel/UCBQsCLHlhKYYIhOJ0eaJ_xA"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('accounts/', include('allauth.urls')),
    path('audio/', include('src.audio_library.urls')),
]
