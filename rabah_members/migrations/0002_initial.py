# Generated by Django 4.2.7 on 2024-03-11 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("rabah_organisations", "0001_initial"),
        ("rabah_members", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="member",
            name="groups",
            field=models.ManyToManyField(blank=True, to="rabah_organisations.group"),
        ),
        migrations.AddField(
            model_name="member",
            name="organisation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="rabah_organisations.organisation",
            ),
        ),
    ]
