# Generated by Django 4.2.11 on 2024-04-28 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_conversationmessage_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversationmessage',
            name='username',
        ),
    ]
