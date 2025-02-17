from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, CommentViewSet, RatingViewSet, RegisterView

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/', include('djoser.urls')),
    path('', include(router.urls)),
    path('', include('rest_framework.urls')),

]