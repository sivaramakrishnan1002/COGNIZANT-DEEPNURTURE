from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, StudentViewSet

router = DefaultRouter()

router.register(r'courses', CourseViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = router.urls