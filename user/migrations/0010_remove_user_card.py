# Generated by Django 4.2.8 on 2023-12-20 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_rename_user_card_user_card'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='card',
        ),
    ]
