# Generated by Django 2.1.3 on 2018-12-05 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parent',
            old_name='citizenship',
            new_name='citizenship_no',
        ),
    ]
