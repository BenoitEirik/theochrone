# Generated by Django 2.1.3 on 2019-09-05 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0010_auto_20181006_0440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='helparticle',
            name='version',
            field=models.CharField(default='0.6.1', max_length=5),
        ),
    ]
