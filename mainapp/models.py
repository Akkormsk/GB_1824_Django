from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    preamble = models.CharField(max_length=1000, verbose_name='Превью')
    body = models.TextField(verbose_name="Содержимое")
    body_as_markdown = models.BooleanField(default=False, verbose_name="Способ разметки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    deleted = models.BooleanField(default=False, verbose_name="Удален")


class Courses(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    preamble = models.CharField(max_length=1000, verbose_name='Краткое описание')
    body = models.TextField(verbose_name="Содержимое")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    deleted = models.BooleanField(default=False, verbose_name="Удален")


class Lessons(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, default='1')
    title = models.CharField(max_length=255, verbose_name='Название')
    preamble = models.CharField(max_length=1000, verbose_name='Краткое описание')
    body = models.TextField(verbose_name="Содержимое")
    length = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Продолжительность мин', default='1')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    deleted = models.BooleanField(default=False, verbose_name="Удален")


class Teachers(models.Model):
    course = models.ManyToManyField(Courses)
    title = models.CharField(max_length=255, verbose_name='ФИО')
    body = models.TextField(verbose_name="О преподавателе")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    deleted = models.BooleanField(default=False, verbose_name="Удален")

    def __str__(self):
        return f'{self.pk} {self.title}'

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "новости"
        ordering = ('-created_at',)
