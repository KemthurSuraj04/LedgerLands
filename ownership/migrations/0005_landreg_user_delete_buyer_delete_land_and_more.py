# Generated by Django 5.1.4 on 2024-12-09 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ownership', '0004_landinspector_email_seller_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Landreg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('area', models.PositiveIntegerField()),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('land_price', models.PositiveIntegerField()),
                ('property_pid', models.PositiveIntegerField(unique=True)),
                ('physical_survey_number', models.PositiveIntegerField()),
                ('ipfs_hash', models.CharField(max_length=255)),
                ('document', models.CharField(max_length=255)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_for_sale', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.PositiveIntegerField()),
                ('city', models.CharField(max_length=255)),
                ('aadhar_number', models.CharField(max_length=12, unique=True)),
                ('pan_number', models.CharField(max_length=10, unique=True)),
                ('document', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Buyer',
        ),
        migrations.DeleteModel(
            name='Land',
        ),
        migrations.DeleteModel(
            name='LandInspector',
        ),
        migrations.DeleteModel(
            name='Seller',
        ),
    ]
