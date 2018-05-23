from rest_framework.routers import DefaultRouter

from api import views

app_name: str = 'api'

router = DefaultRouter()
router.register(r'animal', views.AnimalViewSet, base_name='animal')
router.register(r'herd', views.HerdViewSet, base_name='herd')
urlpatterns = router.urls
