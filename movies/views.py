from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Movie, Comment, Rating
from .serializers import MovieSerializer, CommentSerializer, RatingSerializer,  RegisterSerializer
from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from django.core.paginator import Paginator
from django.shortcuts import render

class MovieFilter(filters.FilterSet):
    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'genre']

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = MovieFilter
    search_fields = ['title', 'description']
    ordering_fields = ['release_date', 'rating_average']

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def upvote(self, request, pk=None):
        comment = self.get_object()
        comment.upvotes += 1
        comment.save()
        return Response({'status': 'Izoh yaxshi baholandi', 'upvotes': comment.upvotes})

    @action(detail=True, methods=['post'])
    def downvote(self, request, pk=None):
        comment = self.get_object()
        comment.downvotes += 1
        comment.save()
        return Response({'status': 'Izoh yomon baholandi', 'downvotes': comment.downvotes})

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

def movie_list(request):
    movie_list = Movie.objects.all()
    paginator = Paginator(movie_list, 10)

    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    return render(request, 'movies/movie_list.html', {'movies': movies})
