from rest_framework import routers
from .views import BuildingViewSet

router = routers.DefaultRouter()
router.register(r'buildings', BuildingViewSet)

urlpatterns = router.urls