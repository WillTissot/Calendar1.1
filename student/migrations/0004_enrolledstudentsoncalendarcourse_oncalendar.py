# Generated by Django 4.1.7 on 2023-05-27 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_enrolledstudentsoncalendarcourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrolledstudentsoncalendarcourse',
            name='onCalendar',
            field=models.BooleanField(default=False, null=True),
        ),
    ]