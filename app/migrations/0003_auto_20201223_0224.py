# Generated by Django 3.1.4 on 2020-12-23 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_add_master_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='pizza',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='pizzatopping',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
