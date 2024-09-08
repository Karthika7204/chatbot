from django.db import models
# Create your models here.
class Feature(models.Model):
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=100)

class intents(models.Model):  # Use PascalCase for class names
    tag = models.CharField(max_length=220)
    patterns = models.TextField()  # Use TextField for large text like lists
    responses = models.TextField()

    def __str__(self):
        return self.tag
