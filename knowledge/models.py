from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    class Tags(models.TextChoices):
        SCIENCE =  "Science"
        INFORMATIVE = "Informative"
        FACT =  "Fact"
        TECH = "Tech"

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField()
    tag = models.CharField(max_length=120, choices=Tags.choices, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Topic.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
        
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} "

 