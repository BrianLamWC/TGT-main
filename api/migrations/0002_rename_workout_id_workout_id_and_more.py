# Generated by Django 4.0.5 on 2022-07-09 14:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workout',
            old_name='workout_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='workout',
            old_name='workout_name',
            new_name='name',
        ),
    ]
