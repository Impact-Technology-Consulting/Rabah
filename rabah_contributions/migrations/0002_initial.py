# Generated by Django 4.2.7 on 2024-03-11 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("rabah_contributions", "0001_initial"),
        ("rabah_organisations", "0001_initial"),
        ("rabah_members", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contributiontype",
            name="organisation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="rabah_organisations.organisation",
            ),
        ),
        migrations.AddField(
            model_name="contribution",
            name="contribution_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="rabah_contributions.contributiontype",
            ),
        ),
        migrations.AddField(
            model_name="contribution",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contribution_created_by",
                to="rabah_members.member",
            ),
        ),
        migrations.AddField(
            model_name="contribution",
            name="member",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contribution_memeber",
                to="rabah_members.member",
            ),
        ),
        migrations.AddField(
            model_name="contribution",
            name="organisation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="rabah_organisations.organisation",
            ),
        ),
    ]
