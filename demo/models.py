from django.db import models

from users.models import User

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    created_at = models.DateField(auto_now_add=True)
    downloaded_at = models.DateField(auto_now=True)
    comment = models.CharField(max_length=50)
    path = models.CharField(max_length=100)
    url = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')



    
    