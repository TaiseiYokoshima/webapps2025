# Generated by Django 5.1.7 on 2025-04-09 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payapp", "0013_rename_receiver_amount_request_sender_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="receiver_amount",
            field=models.DecimalField(decimal_places=2, max_digits=19, null=True),
        ),
    ]
