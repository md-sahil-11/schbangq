from rest_framework.routers import DefaultRouter

from . import views

app_name = "posts"

router = DefaultRouter(trailing_slash=False)

router.register("post-comments/", views.PostCommentViewSet, basename="post-comments")
router.register("", views.PostViewSet, basename="posts")

urlpatterns = router.urls
