# Generated by Django 4.2.14 on 2024-07-23 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0015_alter_tutor_tutoring_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorscheduleitems',
            name='is_reserved',
            field=models.BooleanField(default=False),
        ),
    ]
