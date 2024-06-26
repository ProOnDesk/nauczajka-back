# Generated by Django 4.2.11 on 2024-04-17 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0010_alter_tutor_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='in_person_sessions_available',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tutor',
            name='online_sessions_available',
            field=models.BooleanField(default=False),
        ),
    ]
