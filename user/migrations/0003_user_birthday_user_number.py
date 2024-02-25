# Generated by Django 4.2.8 on 2023-12-18 21:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(default=datetime.date(2023, 1, 1)),
        ),
        migrations.AddField(
            model_name='user',
            name='number',
            field=models.IntegerField(default=0),
        ),
    ]
