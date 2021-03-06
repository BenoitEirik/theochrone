# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-23 20:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0004_auto_20180123_1816'),
    ]

    operations = [
        migrations.AddField(
            model_name='helparticle',
            name='short_description_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='helparticle',
            name='short_description_fr',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='helparticle',
            name='text_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='helparticle',
            name='text_fr',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='helparticle',
            name='title_en',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='helparticle',
            name='title_fr',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
