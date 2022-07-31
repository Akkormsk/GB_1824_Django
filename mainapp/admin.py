from django.contrib import admin
from mainapp.models import News, Courses, Lessons, Teachers

admin.site.register(Teachers)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'deleted', 'slug')
    list_filter = ('deleted', 'created')
    ordering = ('pk',)
    list_per_page = 5
    search_fields = ('title', 'body')
    actions = 'mark_as_deleted',

    def slug(self, obj):
        return obj.title.lower().replace(' ', '_')

    def mark_as_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_deleted.short_description = 'Пометить на удаление'


@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'get_course_name', 'title', 'length', 'deleted', 'slug')
    list_filter = ('deleted', 'created')
    ordering = ('pk',)
    list_per_page = 5
    search_fields = ('title', 'body')
    actions = 'mark_as_deleted',

    def get_course_name(self, obj):
        return obj.course.title

    get_course_name.short_description = "Курс"

    def slug(self, obj):
        return obj.title.lower().replace(' ', '_')

    def mark_as_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_deleted.short_description = 'Пометить на удаление'


@admin.register(Courses)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'deleted', 'slug')
    list_filter = ('deleted', 'created')
    ordering = ('pk',)
    list_per_page = 5
    search_fields = ('title', 'body')
    actions = 'mark_as_deleted',

    def slug(self, obj):
        return obj.title.lower().replace(' ', '_')

    def mark_as_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_deleted.short_description = 'Пометить на удаление'
