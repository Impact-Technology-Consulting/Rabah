# Generated by Django 4.2.7 on 2024-06-11 08:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('rabah_organisations', '0003_organisation_parent_invitation'),
        ('rabah_members', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberInvitation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, to='rabah_organisations.group')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rabah_organisations.organisation')),
            ],
        ),
    ]
