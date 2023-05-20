# Generated by Django 4.1.7 on 2023-05-20 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_alter_course_department_alter_course_professor_and_more'),
        ('event', '0006_remove_event_description_remove_event_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='course',
        ),
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_deleted',
        ),
        migrations.RemoveField(
            model_name='event',
            name='is_online',
        ),
        migrations.RemoveField(
            model_name='event',
            name='professor',
        ),
        migrations.RemoveField(
            model_name='event',
            name='room_number',
        ),
        migrations.RemoveField(
            model_name='event',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='student',
        ),
        migrations.AddField(
            model_name='event',
            name='calendarCourse',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='course.calendarcourse'),
        ),
    ]
