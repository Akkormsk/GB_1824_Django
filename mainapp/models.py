from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy as _

NULLABLE = {'blank': True, 'null': True}


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    deleted = models.BooleanField(default=False, verbose_name="Удален")

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    class Meta:
        abstract = True
        ordering = ('-created',)

    def __str__(self):
        return f'{self.pk}. {self.title}'


# class NewsManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(deleted=False)


class News(BaseModel):
    # objects = NewsManager()
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    preambule = models.CharField(max_length=1000, verbose_name='Превью')
    body = models.TextField(verbose_name="Содержимое")
    body_as_markdown = models.BooleanField(default=False, verbose_name="Способ разметки")

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "новости"


class Courses(BaseModel):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(max_length=1000, verbose_name='Краткое описание')
    body = models.TextField(verbose_name="Содержимое")

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lessons(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название')
    preamble = models.CharField(max_length=1000, verbose_name='Краткое описание')
    body = models.TextField(verbose_name="Содержимое")
    length = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Продолжительность мин', default='1')

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Teachers(BaseModel):
    course = models.ManyToManyField(Courses)
    title = models.CharField(max_length=255, verbose_name='ФИО')
    body = models.TextField(verbose_name="О преподавателе")

    class Meta:
        verbose_name = "учитель"
        verbose_name_plural = "учителя"


class CourseFeedback(BaseModel):
    RATING = ((5, "⭐⭐⭐⭐⭐"), (4, "⭐⭐⭐⭐"), (3, "⭐⭐⭐"), (2, "⭐⭐"), (1, "⭐"))
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, verbose_name="Курс")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Пользователь")
    feedback = models.TextField(default="Пока отзыв пуст", verbose_name="Отзыв")
    rating = models.SmallIntegerField(choices=RATING, default=5, verbose_name="Оценка")

