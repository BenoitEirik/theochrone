# Generated by Django 2.0.4 on 2018-10-06 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0009_auto_20180926_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helparticle',
            name='version',
            field=models.CharField(default='0.6.0', max_length=5),
        ),
    ]
