from rest_framework.routers import DefaultRouter

from . import views

app_name = "workspace"

router = DefaultRouter(trailing_slash=False)

router.register("", views.WorkspaceViewSet, basename="workspaces")

urlpatterns = router.urls
