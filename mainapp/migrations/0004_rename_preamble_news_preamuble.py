# Generated by Django 4.0.4 on 2022-06-18 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_courses_options_alter_lessons_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='preamble',
            new_name='preamuble',
        ),
    ]
