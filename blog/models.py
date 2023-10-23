from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):  # Дає вибір одного з двух параметрів
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    """Створення зовнішнього ключа який відноситься до PrimaryKey таблиці User
    так як один користувач може зробити безліч постів
     "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  # Додати час відразу при створенні нового об'єкту
    update = models.DateTimeField(auto_now=True)  # Час додається кожного разу при збереженні об'єкта
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)  # Статус поста, опубліковано чи ні

    objects = models.Manager()
    published = PublishedManager()

    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']  # За замовчуванням при зверненні до БД повертає дані відсортавані за publish DESC
        indexes = [
            models.Index(fields=['-publish']),  # Додати індекси які відштовхуються вій поля publish
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,  # Повертає /blog/2023/10/19/one-more-post/
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
