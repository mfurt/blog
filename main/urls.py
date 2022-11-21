from .views import PostViewSet,CommentViewSet, TagListView
from rest_framework.routers import DefaultRouter
from django.urls import path
from django.conf.urls import include, url

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')
urlpatterns = router.urls
urlpatterns += [
    path('posts/tag/<tag>', TagListView.as_view()),
    path('auth/', include('rest_auth.urls'))
]


