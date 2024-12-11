from django.db import models

from users.models import User

# Create your models here.
class File(models.Model):
    name = models.CharField(max_length=50)
    size = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    downloaded_at = models.DateField(null=True, blank=True)
    comment = models.CharField(max_length=100,null=True,blank=True)
    path = models.CharField(max_length=100)
    url = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')



    
    