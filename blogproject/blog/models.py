from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self) :
        return self.name 
    
class Post(models.Model):

    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, default=1)
    content = RichTextField(blank=True, null=True)
    image = models.ImageField(upload_to='posts/', default='standard.jpg')
    date_potsed = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    #TO ASSOCIATE DIFF THINGS FROM DIFF TABLES
    likes = models.ManyToManyField(User, related_name='blog_post')

    def total_likes(self):
        return self.likes.count()
    def __str__(self)  :
        return self.title + ' | ' + str(self.author)
    
    #get absolute url to add post
    def get_absolute_url(self):
        return reverse('article', args=(str(self.id)))
        # return reverse('home')
