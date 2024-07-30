
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutoringreservation',
            name='is_confirmed',
            field=models.BooleanField(default=True),
        ),
    ]
