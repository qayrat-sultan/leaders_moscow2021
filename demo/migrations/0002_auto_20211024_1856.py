# Generated by Django 3.2.8 on 2021-10-24 18:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 10, 24, 18, 56, 37, 730795, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='file',
            name='returned_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
