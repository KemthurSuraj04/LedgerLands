# Generated by Django 5.1.4 on 2024-12-08 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ownership', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seller',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
