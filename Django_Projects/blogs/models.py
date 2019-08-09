from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ This is to redirect the new post page and to display that post as a confirmation."""
        return reverse('Blog-Home')  ## After creating the new post and get back to home page
        # return reverse('post-detail',kwargs = {'pk':self.pk} ) # and this will get back to detail page
