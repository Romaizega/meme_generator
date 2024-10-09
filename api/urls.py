from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import MemeTemplateViewSet, UserViewSet

app_name = 'api'

router = DefaultRouter()


router.register('users', UserViewSet, 'users')
router.register('templates', MemeTemplateViewSet, 'templates')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
