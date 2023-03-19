from django.db import models

# Create your models here.
class Review(models.Model):
  review_CHOICES = (
        ('5', 'Amazing'),
        ('3', 'Decent'),
        ('1', 'Disappointing'),
    )
  name = models.CharField(default="", max_length=15)
  food = models.CharField(default="",max_length=1, choices=review_CHOICES)
  speed = models.CharField(default="",max_length=1, choices=review_CHOICES)
  price = models.CharField(default="",max_length=1, choices=review_CHOICES)

  text = models.TextField(blank = True)

  def __str__(self):
    return self.name