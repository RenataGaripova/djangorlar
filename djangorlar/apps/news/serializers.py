import abc
import math

from rest_framework import serializers
from .models import Article, Category, Tag, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class UserPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "get_full_name")
        read_only_fields = fields


class TagSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="news:tag-detail", lookup_field="slug")

    class Meta:
        model = Tag
        fields = ("id", "name",  "url")
        read_only_fields = ("id", "slug")


class CategorySerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="news:category-detail", lookup_field="slug")

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "url")
        read_only_fields = ("id", "slug")


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "article", "user", "name", "email", "body", "approved", "created_at", "deleted_at")
        read_only_fields = ("id", "approved", "created_at")

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["user"] = request.user
            validated_data.pop("email", None)
            validated_data.pop("name", None)
        return super().create(validated_data)


class ArticleListSerializer(serializers.ModelSerializer):
    author = UserPreviewSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="news:article-detail", lookup_field="slug")

    class Meta:
        model = Article
        fields = ("id", "title", "slug", "summary", "author", "category", "tags", "published", "publish_at", "is_featured", "url")
        ead_only_fields = ("id", "slug", "author")


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserPreviewSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Article
        exclude = ()
        read_only_fields = ("id", "slug", "author", "created_at", "updated_at")

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.get_absolute_url())
        return obj.get_absolute_url()


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    tag_names = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)

    class Meta:
        model = Article
        fields = ("title", "summary", "content", "category", "tag_names", "publish_at", "is_featured", "hero_image")

    def create(self, validated_data):
        tag_names = validated_data.pop("tag_names", [])
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["author"] = request.user
        article = super().create(validated_data)
        if tag_names:
            tags = []
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            article.tags.set(tags)
        return article

    def update(self, instance, validated_data):
        tag_names = validated_data.pop("tag_names", None)
        instance = super().update(instance, validated_data)
        if tag_names is not None:
            tags = [Tag.objects.get_or_create(name=n)[0] for n in tag_names]
            instance.tags.set(tags)
        return instance
