# Generated by Django 3.2.3 on 2021-05-27 16:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagefood',
            name='religion',
            field=models.CharField(choices=[(datetime.time(10, 0), datetime.time(10, 0)), (datetime.time(16, 0), datetime.time(16, 0))], max_length=150),
        ),
    ]
