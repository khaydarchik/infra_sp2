from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserCreate, UserToken, UserViewSet

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews_title'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)'
    r'/comments/(?P<comment_id>[\d]+)',
    CommentViewSet,
    basename='comments_detail'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', UserToken.as_view(), name='token_obtain'),
    path('v1/auth/signup/', UserCreate.as_view(), name='user_create'),
]
