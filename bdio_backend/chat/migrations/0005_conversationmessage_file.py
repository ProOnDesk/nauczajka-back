# Generated by Django 4.2.13 on 2024-07-06 13:48

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_conversationmessage_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationmessage',
            name='file',
            field=models.FileField(null=True, upload_to=chat.models.get_upload_conversation_message_file_path),
        ),
    ]
