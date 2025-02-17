from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    genre = models.CharField(max_length=100, default='Unknown')
    rating_average = models.FloatField(default=0)
    poster = models.ImageField(upload_to='movie_posters/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    movie = models.ForeignKey(Movie, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, null=True)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  

    def save(self, *args, **kwargs):
        if not isinstance(self.score, int):
            raise ValueError("Score must be an integer.") #Baholash butun son bo‘lishi kerak.
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('movie', 'user')  
