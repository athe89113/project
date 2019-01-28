# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_knowledge', '0006_auto_20181016_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alarmrule',
            name='time',
        ),
        migrations.AddField(
            model_name='alarmrule',
            name='time_type',
            field=models.IntegerField(default=-1, verbose_name='\u65f6\u95f4\u95f4\u9694\u7c7b\u578b'),
        ),
        migrations.AlterField(
            model_name='alarmlog',
            name='group_name',
            field=models.CharField(max_length=100, null=True, verbose_name='\u89c4\u5219\u7ec4\u540d\u79f0', blank=True),
        ),
    ]
