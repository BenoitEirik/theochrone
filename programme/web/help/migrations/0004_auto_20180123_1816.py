# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-23 18:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0003_auto_20180123_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='helparticle',
            name='version_major',
        ),
        migrations.RemoveField(
            model_name='helparticle',
            name='version_minor',
        ),
        migrations.RemoveField(
            model_name='helparticle',
            name='version_patch',
        ),
        migrations.AddField(
            model_name='helparticle',
            name='version',
            field=models.CharField(default='0.5.0', max_length=5),
        ),
    ]