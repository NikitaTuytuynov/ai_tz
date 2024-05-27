from django.db import models

class Image(models.Model):
  CATEGORY_CHOICES = [
    ('food', 'Food'),
    ('nature', 'Nature'),
    ('city', 'City')
  ]

  # save image to media folder
  image = models.ImageField(upload_to='images/')
  category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

  def __str__(self):
    return self.category
