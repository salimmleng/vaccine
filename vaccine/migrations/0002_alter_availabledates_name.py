# Generated by Django 5.0.6 on 2024-08-02 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availabledates',
            name='name',
            field=models.DateField(),
        ),
    ]
