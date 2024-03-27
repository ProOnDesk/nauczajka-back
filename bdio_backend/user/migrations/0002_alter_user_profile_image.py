# Generated by Django 4.2.11 on 2024-03-27 15:15

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='uploads/user/default.jpg', null=True, upload_to=user.models.get_upload_user_path),
        ),
    ]