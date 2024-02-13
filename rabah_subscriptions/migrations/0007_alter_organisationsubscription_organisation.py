# Generated by Django 4.2.7 on 2024-02-12 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rabah_organisations', '0003_alter_group_options_alter_organisation_options'),
        ('rabah_subscriptions', '0006_organisationsubscription_free_tier_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisationsubscription',
            name='organisation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rabah_organisations.organisation'),
        ),
    ]
