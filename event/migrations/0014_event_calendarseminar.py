# Generated by Django 4.1.7 on 2023-06-05 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seminar', '0002_enrolledstudenttocalendarseminars'),
        ('event', '0013_change_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='calendarSeminar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='seminar.calendarseminar'),
        ),
    ]
