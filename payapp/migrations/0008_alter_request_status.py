# Generated by Django 5.1.7 on 2025-03-22 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0007_alter_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('D', 'Denied')], default='P', max_length=1),
        ),
    ]
