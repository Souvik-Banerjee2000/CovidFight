from django.db import models
from usermanagement.models import UserProfile
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(UserProfile,on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class Answer(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    reply = models.TextField()
    upvote = models.IntegerField(default = 0)
    downvote = models.IntegerField(default = 0)
    post = models.ForeignKey(Post,related_name='Reply',on_delete=models.CASCADE)

    def __str__(self):
        return self.reply
        
    