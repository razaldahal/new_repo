# Generated by Django 2.1.3 on 2018-12-04 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('Section', '0001_initial'),
        ('teacher', '0001_initial'),
        ('Class', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachersection',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Subject'),
        ),
        migrations.AddField(
            model_name='teachersection',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher'),
        ),
        migrations.AddField(
            model_name='sectionstudent',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Section.Section'),
        ),
        migrations.AddField(
            model_name='sectionstudent',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Student'),
        ),
        migrations.AddField(
            model_name='sectionroutine',
            name='teacher_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Section.TeacherSection'),
        ),
        migrations.AddField(
            model_name='section',
            name='_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Class.Class'),
        ),
    ]
