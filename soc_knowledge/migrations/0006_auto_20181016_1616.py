# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_knowledge', '0005_auto_20181016_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarmrule',
            name='content',
            field=models.TextField(null=True, verbose_name='\u67e5\u8be2\u6761\u4ef6', blank=True),
        ),
        migrations.AlterField(
            model_name='alarmlog',
            name='alarm_level',
            field=models.IntegerField(default=0, verbose_name='\u4e8b\u4ef6\u7ea7\u522b'),
        ),
        migrations.AlterField(
            model_name='alarmrule',
            name='interval',
            field=models.IntegerField(default=0, verbose_name='\u65f6\u95f4\u95f4\u9694'),
        ),
        migrations.AlterField(
            model_name='alarmrule',
            name='level',
            field=models.IntegerField(default=0, verbose_name='\u7b49\u7ea7'),
        ),
        migrations.AlterField(
            model_name='alarmrule',
            name='sql',
            field=models.TextField(null=True, verbose_name='\u62fc\u88c5sql', blank=True),
        ),
        migrations.AlterField(
            model_name='alarmrule',
            name='status',
            field=models.IntegerField(default=-1, verbose_name='\u72b6\u6001'),
        ),
        migrations.AlterField(
            model_name='alarmrule',
            name='time',
            field=models.IntegerField(default=-1, verbose_name='\u65f6\u95f4\u95f4\u9694\u72b6\u6001'),
        ),
    ]
