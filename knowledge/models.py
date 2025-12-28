from django.db import models
from django.utils.text import slugify


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null = True)
    description = models.TextField()

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

 