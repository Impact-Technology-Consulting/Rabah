# Generated by Django 4.2.7 on 2024-02-05 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rabah_members', '0004_alter_member_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['-timestamp']},
        ),
    ]
