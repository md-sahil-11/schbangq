from rest_framework.routers import DefaultRouter

from . import views

app_name = "users"

router = DefaultRouter(trailing_slash=False)

router.register("account", views.UserViewSet, basename="account")

urlpatterns = router.urls
