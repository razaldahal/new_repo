# Generated by Django 2.1.4 on 2019-01-02 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0007_classteacherallocation'),
        ('teacher', '0002_auto_20190102_0831'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('date_deleted', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Subject')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('date_deleted', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=30)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Batch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='schedule',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.Term'),
        ),
    ]