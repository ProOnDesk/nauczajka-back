# Generated by Django 4.2.11 on 2024-03-29 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0003_alter_tutor_avg_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
