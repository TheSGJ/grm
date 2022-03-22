from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField
# Create your models here.
class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    author=models.CharField(max_length=199)
    slug=models.CharField(max_length=130)
    timeStamp=models.DateTimeField(blank=True)
    desc=HTMLField()
    content=models.CharField(max_length=2550)
    img=models.CharField(max_length=2550)

    def __str__(self):
        return self.title + " by " + self.author

class TvComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
