# Generated by Django 4.2.14 on 2024-07-31 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0003_alter_respond_issue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='category',
            field=models.CharField(choices=[('violation', 'Naruszenie Regulaminu'), ('technical_issue', 'Problem Techniczny'), ('help_request', 'Prośba o Pomoc')], max_length=50),
        ),
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('new', 'Nowe'), ('in_progress', 'W Trakcie'), ('resolved', 'Rozwiązane'), ('closed', 'Zamknięte')], default='new', max_length=20),
        ),
    ]
