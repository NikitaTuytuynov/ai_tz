from django.db import models

class Image(models.Model):
  CATEGORY_CHOICES = [
    ('food', 'Food'),
    ('nature', 'Nature'),
    ('city', 'City')
  ]

  category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
  image = models.ImageField(upload_to='images/')

  def __str__(self):
    return self.category
