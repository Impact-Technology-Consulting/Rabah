# Generated by Django 4.2.7 on 2024-01-19 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabah_events', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, upload_to='events'),
        ),
    ]