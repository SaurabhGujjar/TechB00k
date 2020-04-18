from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    writer = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Category', related_name='posts')

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


    def __str__(self):
        cmt = self.author + self.body
        return cmt


class ReplyComment(models.Model):
    reply_author = models.CharField(max_length=60)
    reply_body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    cmnt = models.ForeignKey("Comment", on_delete=models.CASCADE)

    def __str__(self):
        reply = self.reply_author + self.reply_body
        return reply



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pro_pic = models.ImageField(upload_to='pro_pic', blank=True, null=False)
    about = models.TextField(blank=True, null=False)
    skills = models.CharField(max_length=500, blank=True, null=False)
    linkdin = models.CharField(max_length=500, blank=True, null=False)
    github = models.CharField(max_length=500, blank=True, null=False)
    
    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def user_is_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
