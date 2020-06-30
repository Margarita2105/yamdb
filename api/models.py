from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="reviews")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    
    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created = models.DateTimeField("Дата добавления", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text