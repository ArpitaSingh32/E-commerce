# Generated by Django 3.2.4 on 2023-09-20 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_myorders'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myorders',
            name='order_date',
            field=models.DateField(null=True),
        ),
    ]
