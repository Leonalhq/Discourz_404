# Generated by Django 2.1.1 on 2018-11-01 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discourz_app', '0002_polltopic_voters'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='firstName',
            field=models.TextField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='account',
            name='lastName',
            field=models.TextField(default='', max_length=500),
        ),
    ]
