# Generated by Django 4.2.7 on 2024-01-29 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabah_events', '0004_event_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='repeat',
            field=models.CharField(blank=True, choices=[('NEVER', 'NEVER'), ('DAILY', 'DAILY'), ('WEEKLY', 'WEEKLY'), ('MONTHLY', 'MONTHLY'), ('YEARLY', 'YEARLY')], max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='repeat_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
