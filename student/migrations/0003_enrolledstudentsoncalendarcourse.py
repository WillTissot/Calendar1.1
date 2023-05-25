# Generated by Django 4.1.7 on 2023-05-25 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_alter_semester_term'),
        ('student', '0002_alter_student_department_enrolledstudentsoncourse'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnrolledStudentsOnCalendarCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendarCourse', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.calendarcourse')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student.student')),
            ],
        ),
    ]
