import math
import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

default_time = datetime.datetime.now()


class TimeStampedModel(models.Model):
    """Abstract base class that provides created/modified timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField()

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news:category-detail-super", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=76, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:60]
        super().save(*args, **kwargs)


class ArticleQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(published=True, publish_at__lte=now)

    def featured(self):
        return self.filter(is_featured=True)


class Article(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="articles")
    title = models.CharField(max_length=455)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="articles")
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")

    # publication controls
    published = models.BooleanField(default=False)
    publish_at = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=False)

    # optional hero image
    hero_image = models.ImageField(upload_to="news/hero_images/", null=True, blank=True)

    objects = ArticleQuerySet.as_manager()

    class Meta:
        ordering = ["-publish_at", "-created_at"]
        indexes = [models.Index(fields=["slug"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:258]
            slug = base
            counter = 0
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news:article-detail", kwargs={"slug": self.slug})


class Comment(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, related_name="comments", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    body = models.TextField()
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment by user {self.name or self.user or 'Anonymous'} on {self.article}"
