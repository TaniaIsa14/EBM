# Generated by Django 3.2.3 on 2021-05-20 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='name',
            field=models.TextField(default='asf', max_length=150),
            preserve_default=False,
        ),
    ]
