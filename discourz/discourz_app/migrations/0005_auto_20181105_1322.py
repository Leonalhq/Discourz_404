# Generated by Django 2.1.3 on 2018-11-05 18:22

import discourz_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discourz_app', '0004_auto_20181103_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='polltopic',
            name='img',
            field=models.ImageField(default='static/img/img/default.jpg', upload_to=discourz_app.models.poll_directory_path),
        ),
    ]