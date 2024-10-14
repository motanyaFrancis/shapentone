from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


# Create your models here.

class PostCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(_("slug"), null=True, blank=True, unique=True, default='', editable=False)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = HTMLField()
    image = models.FileField()
    category = models.ForeignKey(PostCategory, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(_("slug"), null=True, blank=True, unique=True, default='', editable=False)
    published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category.title + '-' + self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

