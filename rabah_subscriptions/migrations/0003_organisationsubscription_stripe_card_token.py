# Generated by Django 4.2.7 on 2024-02-12 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabah_subscriptions', '0002_subscription_stripe_plan_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisationsubscription',
            name='stripe_card_token',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
