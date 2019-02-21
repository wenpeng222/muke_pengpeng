# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-15 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20181231_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifiyrecord',
            name='send_type',
            field=models.CharField(choices=[('regiser', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')], max_length=10, verbose_name='验证码类型'),
        ),
    ]
