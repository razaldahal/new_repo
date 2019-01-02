# Generated by Django 2.1.4 on 2019-01-01 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('date_deleted', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('progress', models.FloatField()),
                ('status', models.CharField(max_length=50)),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('date_deleted', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.Event')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]