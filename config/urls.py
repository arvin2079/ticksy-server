from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="TickSy API",
      default_version='v1',
      description="A Ticketing application",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="amiralifmj@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    # admin panel
    path('admin/', admin.site.urls),

    # REST FRAMEWORK API URLS
    path('api/auth/', include('users.api.urls', 'auth-api')),

    # documentations
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


app_name = "TickSy"  # You can reference the name from another file...
admin.site.site_header = "پنل مدیریت " + app_name
admin.site.site_title = app_name
admin.site.index_title = "صفحه مدیریت"
