# Generated by Django 2.0.7 on 2018-09-10 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Section', '0004_auto_20180910_0642'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('date_deleted', models.DateField(blank=True, null=True)),
                ('due_date', models.DateField()),
                ('priority', models.CharField(max_length=120)),
                ('status', models.IntegerField(choices=[('SUBMITTED', 1), ('PENDING', 2)])),
                ('name', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=120)),
                ('teacher_sec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Section.TeacherSection')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('date_deleted', models.DateField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[('SUBMITTED', 1), ('PENDING', 2)])),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment.Assignment')),
                ('section_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Section.SectionStudent')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
