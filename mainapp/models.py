from django.db import models

NULLABLE = {'blank': True, 'null': True}


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    deleted = models.BooleanField(default=False, verbose_name="Удален")

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    class Meta:
        # app_label = 'mainapp'
        abstract = True
        ordering = ('-created',)


class NewsManager(models.Manager):
    def delete(self):
        pass

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class News(BaseModel):
    objects = NewsManager()
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    preambule = models.CharField(max_length=1000, verbose_name='Превью')
    body = models.TextField(verbose_name="Содержимое")
    body_as_markdown = models.BooleanField(default=False, verbose_name="Способ разметки")

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "новости"
        # app_label = 'mainapp'

    def __str__(self):
        return f'{self.pk} {self.title}'


class Courses(BaseModel):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(max_length=1000, verbose_name='Краткое описание')
    body = models.TextField(verbose_name="Содержимое")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        # app_label = 'mainapp'


class Lessons(BaseModel):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, default='1')
    title = models.CharField(max_length=255, verbose_name='Название')
    preamble = models.CharField(max_length=1000, verbose_name='Краткое описание')
    body = models.TextField(verbose_name="Содержимое")
    length = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Продолжительность мин', default='1')

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        # app_label = 'mainapp'


class Teachers(BaseModel):
    course = models.ManyToManyField(Courses)
    title = models.CharField(max_length=255, verbose_name='ФИО')
    body = models.TextField(verbose_name="О преподавателе")

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"
        # app_label = 'mainapp'
