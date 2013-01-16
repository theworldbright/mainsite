from django.db import models
from datetime import datetime

class Listing(models.Model):
    title = models.CharField(max_length=120)
    posted = datetime.now
    author = models.CharField(max_length=30)
    contact = models.CharField(max_length=30)
    price = models.CharField(max_length=6)
    content = models.TextField()
    image = models.ImageField(upload_to='listings_pics')
