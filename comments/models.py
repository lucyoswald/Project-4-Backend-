from django.db import models

# Create your models here.
class Comment(models.Model):
    text = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        "posts.Post",  
        related_name="comments",  
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        "jwt_auth.User",
        on_delete=models.CASCADE
    )


    def __str__(self):  
         return f"{self.text} - {self.post}"