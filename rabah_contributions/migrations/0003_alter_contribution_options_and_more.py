# Generated by Django 4.2.7 on 2024-02-07 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rabah_contributions', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contribution',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='contributiontype',
            options={'ordering': ['-timestamp']},
        ),
    ]
