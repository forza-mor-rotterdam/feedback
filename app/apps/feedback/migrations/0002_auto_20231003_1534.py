# Generated by Django 3.2.16 on 2023-10-03 13:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='update_datum',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='meldr_nummer',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
