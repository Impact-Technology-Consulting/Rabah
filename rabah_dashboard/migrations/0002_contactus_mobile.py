# Generated by Django 4.2.7 on 2024-10-16 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabah_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='mobile',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
