# Generated by Django 2.1.3 on 2018-12-05 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='syllabus_name',
        ),
    ]
