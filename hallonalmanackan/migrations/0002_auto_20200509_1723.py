# Generated by Django 3.0.6 on 2020-05-09 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hallonalmanackan', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='holiday',
            unique_together={('year', 'month', 'day')},
        ),
    ]
