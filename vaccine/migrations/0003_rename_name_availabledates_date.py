# Generated by Django 5.0.6 on 2024-08-02 06:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0002_alter_availabledates_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='availabledates',
            old_name='name',
            new_name='date',
        ),
    ]
