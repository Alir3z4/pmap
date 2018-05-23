from rest_framework.routers import DefaultRouter

from api import views

app_name: str = 'api'

router = DefaultRouter()
router.register(r'animal', views.AnimalViewSet, base_name='animal')
urlpatterns = router.urls
