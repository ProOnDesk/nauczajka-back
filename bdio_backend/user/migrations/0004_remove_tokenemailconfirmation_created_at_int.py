# Generated by Django 4.2.11 on 2024-03-24 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_tokenemailconfirmation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tokenemailconfirmation',
            name='created_at_int',
        ),
    ]
