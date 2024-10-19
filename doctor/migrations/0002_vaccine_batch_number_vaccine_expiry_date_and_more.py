# Generated by Django 5.0.6 on 2024-07-14 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccine',
            name='batch_number',
            field=models.CharField(default='default-batch-number', max_length=100),
        ),
        migrations.AddField(
            model_name='vaccine',
            name='expiry_date',
            field=models.DateField(default=datetime.date(2024, 12, 31)),
        ),
        migrations.AddField(
            model_name='vaccine',
            name='manufacturer',
            field=models.CharField(default='default-manufacturer', max_length=100),
        ),
    ]
