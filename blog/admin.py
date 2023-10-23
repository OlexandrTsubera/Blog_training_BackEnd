from django.contrib import admin
from .models import Post, Comment


# Декоратор виповнює те саме, що admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']  # Поля які будуть показуватися в адмін-панелі
    list_filter = ['status', 'created', 'publish', 'author']  # Поля за якими буде змога робити фільтрацію
    search_fields = ['title', 'body']  # Список полів за якими буде відбуватися пошук в адмін-панелі
    prepopulated_fields = {'slug': ('title',)}  # Автоматичне зповнення поля slug по даних з поля title
    raw_id_fields = ['author']  # Поле author тепер відображується як пося пошуку
    date_hierarchy = 'publish'  # Додавання змоги сортувати пости по даті опублікування
    ordering = ['status', 'publish']  # Сортування постів за замовчуванням


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'update']
    search_fields = ['name', 'email', 'body']






