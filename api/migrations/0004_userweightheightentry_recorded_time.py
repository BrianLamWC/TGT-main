# Generated by Django 4.0.5 on 2022-07-12 08:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_userweightheightentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='userweightheightentry',
            name='recorded_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 12, 8, 18, 31, 490120, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
