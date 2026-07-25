from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

class Post(models.Model):
    class PostStatus(models.IntegerChoices):
        DRAFT = 0, "Draft"
        PUBLISHED = 1, "Publish"

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = RichTextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=PostStatus.choices, default=PostStatus.DRAFT)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[self.slug])
