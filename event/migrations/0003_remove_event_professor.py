# Generated by Django 4.1.7 on 2023-04-15 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_event_alter_enrollment_unique_together_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='professor',
        ),
    ]
