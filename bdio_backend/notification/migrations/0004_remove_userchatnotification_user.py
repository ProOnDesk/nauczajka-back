# Generated by Django 4.2.14 on 2024-08-01 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_userchatnotification_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userchatnotification',
            name='user',
        ),
    ]
