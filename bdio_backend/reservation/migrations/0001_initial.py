# Generated by Django 4.2.14 on 2024-07-27 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tutor', '0016_tutorscheduleitems_is_reserved'),
    ]

    operations = [
        migrations.CreateModel(
            name='TutoringReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('schedule_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_reservations', to='tutor.tutorscheduleitems')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tutor_reservations', to='tutor.tutor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'schedule_item')},
            },
        ),
    ]
