# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-18 15:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfavorite',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
    ]
