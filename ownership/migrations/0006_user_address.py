# Generated by Django 5.1.4 on 2024-12-09 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ownership', '0005_landreg_user_delete_buyer_delete_land_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
