# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-12-31 15:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20181230_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifiyrecord',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='发送时间'),
        ),
        migrations.AlterField(
            model_name='emailverifiyrecord',
            name='send_type',
            field=models.CharField(choices=[('regiser', '注册'), ('forget', '找回密码')], max_length=10, verbose_name='验证码类型'),
        ),
    ]
