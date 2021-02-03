from rest_framework.routers import DefaultRouter

from apps.blog import views

router = DefaultRouter()
router.register('article', views.ArticleAPIView, basename="article")

urlpatterns = router.urls
