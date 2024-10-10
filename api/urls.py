from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from api.views import (MemeTemplateViewSet, MemeUserViewSet, MemeViewSet,
                       RandomMemeViewSet, RatingViewSet)

app_name = 'api'

router = DefaultRouter()


router.register('users', MemeUserViewSet, 'users')
router.register('templates', MemeTemplateViewSet, 'templates')
router.register('rate', RatingViewSet, 'rate')
router.register('memes', MemeViewSet, 'memes')
router.register('random' , RandomMemeViewSet, 'random')


schema_view = get_schema_view(
   openapi.Info(
      title="Meme Generator API",
      default_version='v1',
      description="API for creating and rating memes",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
    
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
