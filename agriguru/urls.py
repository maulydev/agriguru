from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from accounts.views import ProfileViewSet
from produce.views import ProduceViewSet
from purchase_request.views import PurchaseRequestViewSet, PurchaseResponseViewSet
from posts.views import PostViewSet



schema_view = get_schema_view(
    openapi.Info(
        title="AgriGuru API",
        default_version='v1',
        description="API for AgriGuru",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'produces', ProduceViewSet)
router.register(r'posts', PostViewSet)
router.register(f'purchase-request', PurchaseRequestViewSet)
router.register(f'purchase-response', PurchaseResponseViewSet)


admin.site.index_title = "AgriGuru Administration"
admin.site.name = "AgriGuru"
admin.site.site_header = "AgriGuru"
admin.site.site_title = "Dashboard"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)