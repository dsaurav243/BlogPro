from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status = 'published')

class Blog(models.Model):

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published')
    )

    title = models.CharField(max_length=256)
    slug =  models.SlugField(max_length=256,unique_for_date='publish')
    author = models.ForeignKey(User,related_name='blog_post',on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices= STATUS_CHOICES, default='draft')
    objects =  CustomManager()
    tags = TaggableManager()



    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail_view',args = [self.publish.strftime('%Y'),self.publish.strftime('%m'),self.publish.strftime('%d'),self.slug])


class Comment(models.Model):
    post =  models.ForeignKey(Blog, on_delete= models.CASCADE, related_name='comments')
    name  = models.CharField(max_length=50)
    email =  models.EmailField(max_length=50)
    body =  models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    active  = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return "Commented by {} on {}".format(self.name,self.created_on)
