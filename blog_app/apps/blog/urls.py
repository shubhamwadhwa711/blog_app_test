from rest_framework.routers import DefaultRouter

from apps.blog import views

router = DefaultRouter()
router.register('login', views.UserLoginAPI, basename="login")
router.register('article', views.ArticleAPIView, basename="article")
router.register('article-status', views.ArticleStatusAPIView, basename="article_status_update")

urlpatterns = router.urls
