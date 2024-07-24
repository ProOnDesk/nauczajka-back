# Generated by Django 4.2.14 on 2024-07-23 19:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0015_alter_tutor_tutoring_location'),
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutoringreservation',
            name='schedule_item',
        ),
        migrations.AlterField(
            model_name='tutoringreservation',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutor_reservations', to='tutor.tutor'),
        ),
        migrations.AddField(
            model_name='tutoringreservation',
            name='schedule_item',
            field=models.ManyToManyField(related_name='schedule_reservations', to='tutor.tutorscheduleitems'),
        ),
    ]
