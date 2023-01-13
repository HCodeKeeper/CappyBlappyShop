from django.urls import include, path
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'', views.ProfileView)
urlpatterns = router.urls
