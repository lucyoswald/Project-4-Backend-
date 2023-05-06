from django.db import models

class Post(models.Model):
    image = models.CharField(max_length=300)
    item = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    contact = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    status=models.CharField(max_length=20)

    owner = models.ForeignKey(
         'jwt_auth.User',
         related_name='posts',
         on_delete=models.CASCADE
    )


    def __str__(self):  
         return f"{self.item} - {self.description}"