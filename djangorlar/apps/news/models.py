from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils import encoding
User = get_user_model()


class TimeStampedModel(models.Model):
    """Abstract class that provides created/modified timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "cAtegories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news:category-detail", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=89, unique=True, blank=True)

    class Meta:
        ordering = ["id"]

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
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    summary = models.TextField(blank=False)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="articles")
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")

    # publication controls
    published = models.BooleanField(default=True)
    publish_at = models.DateTimeField(default=timezone.now)
    is_featured = models.BooleanField(default=True)

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
            base = slugify(self.title)[:777]
            slug = base
            # ensure uniqueness
            counter = 0
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base}-{counter}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news:article-detail", kwargs={"slug": self.slug})


class Comment(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    body = models.TextField()
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["updated_at"]

    def __str__(self):
        return f"Comment by {self.name or self.user or 'Anonymous'} on {self.article}"
