# Generated by Django 4.2.14 on 2024-07-17 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_alter_user_oauth2_picture_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_oauth2',
            field=models.BooleanField(default=False),
        ),
    ]
