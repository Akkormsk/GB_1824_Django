# Generated by Django 4.0.4 on 2022-06-18 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_alter_courses_options_alter_lessons_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courses',
            old_name='preamble',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='courses',
            old_name='title',
            new_name='name',
        ),
    ]
