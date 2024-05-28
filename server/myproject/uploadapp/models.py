from django.db import models

class Image(models.Model):
  CATEGORY_CHOICES = [
    ('food', 'Food'),
    ('nature', 'Nature'),
    ('city', 'City')
  ]

  image = models.ImageField(upload_to='images/')
  categoryByUser = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

  def __str__(self):
    return self.category
