# Generated by Django 4.2 on 2023-06-07 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_location'),
        ('identity', '0004_passwordresettoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='location',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='rooms.location'),
        ),
    ]