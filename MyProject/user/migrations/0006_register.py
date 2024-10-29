# Generated by Django 3.2.4 on 2023-09-13 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_myproduct_product_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='register',
            fields=[
                ('name', models.CharField(max_length=150, null=True)),
                ('email', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('mobile', models.CharField(max_length=30, null=True)),
                ('passwd', models.CharField(max_length=100, null=True)),
                ('profile', models.ImageField(null=True, upload_to='static/userpic/')),
                ('address', models.TextField()),
            ],
        ),
    ]
