# Generated by Django 5.1.7 on 2025-03-21 18:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0002_transfer_delete_transaction_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('transfer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payapp.transfer')),
                ('state', models.CharField(choices=[('P', 'Pending'), ('D', 'Denied'), ('A', 'Approve')], default='P', max_length=1)),
            ],
            bases=('payapp.transfer',),
        ),
        migrations.RemoveIndex(
            model_name='transfer',
            name='payapp_tran_sender__a58f98_idx',
        ),
        migrations.RemoveField(
            model_name='transfer',
            name='fee',
        ),
        migrations.AlterField(
            model_name='transfer',
            name='rate',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=19),
        ),
        migrations.AddIndex(
            model_name='transfer',
            index=models.Index(fields=['sender', 'receiver', 'date', 'amount'], name='payapp_tran_sender__1e7b38_idx'),
        ),
    ]
