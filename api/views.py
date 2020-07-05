from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Review, Comment, Title
from .permissions import IsOwnerOrReadOnly
from .serializers import ReviewSerializer, CommentSerializer, TitleSerializer
from users.models import User
from users.serializers import UserSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsOwnerOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        if request.method == 'POST' and Review.objects.filter(user=self.request.user, title=title).exists():
            raise ValidationError('Вы уже поставили оценку')
        serializer.save(author=self.request.user, title=title)
        agg_score = Review.objects.filter(title=title).agregate(Avg('score'))
        title.rating = agg_score['score__avg']
        title.save(update_fields=['rating'])

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['title_id'])
        return Review.objects.filter(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return Comment.objects.filter(review=review)


class UserRegistrationViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny,]