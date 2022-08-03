from rest_framework.routers import DefaultRouter

from . import views

app_name = "workspace"

router = DefaultRouter(trailing_slash=False)

router.register("dashboard", views.WorkspaceViewSet, basename="dashboard")
router.register("service", views.ServiceViewSet, basename="services")
router.register("case-study", views.CaseStudyViewSet, basename="case_studies")

urlpatterns = router.urls
