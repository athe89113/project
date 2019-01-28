# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_knowledge', '0004_smwordlogmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlarmLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=100, null=True, verbose_name='\u89c4\u5219\u79df\u540d\u79f0', blank=True)),
                ('rule_name', models.CharField(max_length=100, null=True, verbose_name='\u89c4\u5219\u540d\u79f0', blank=True)),
                ('src_ip', models.CharField(max_length=50, null=True, verbose_name='\u6e90ip', blank=True)),
                ('src_port', models.CharField(max_length=10, null=True, verbose_name='\u6e90\u7aef\u53e3', blank=True)),
                ('tran_protocol', models.CharField(max_length=50, null=True, verbose_name='\u4f20\u8f93\u5c42\u534f\u8bae', blank=True)),
                ('app_protocol', models.CharField(max_length=50, null=True, verbose_name='\u5e94\u7528\u5c42\u534f\u8bae', blank=True)),
                ('dst_ip', models.CharField(max_length=50, null=True, verbose_name='\u76ee\u7684ip', blank=True)),
                ('dst_port', models.CharField(max_length=10, null=True, verbose_name='\u76ee\u7684\u7aef\u53e3', blank=True)),
                ('event_host', models.CharField(max_length=50, null=True, verbose_name='\u53d1\u73b0\u653b\u51fb\u884c\u4e3a\u8bbe\u5907ip', blank=True)),
                ('event_time', models.DateTimeField(null=True, verbose_name='\u4e8b\u4ef6\u53d1\u751f\u65f6\u95f4', blank=True)),
                ('alarm_time', models.DateTimeField(null=True, verbose_name='\u544a\u8b66\u65f6\u95f4', blank=True)),
                ('alarm_level', models.IntegerField(default=0, max_length=2, verbose_name='\u4e8b\u4ef6\u7ea7\u522b')),
                ('old_log_list', models.TextField(null=True, verbose_name='\u539f\u59cb\u65e5\u5fd7id\u96c6\u5408', blank=True)),
                ('event_source', models.CharField(max_length=10, null=True, verbose_name='\u8bbe\u5907\u7c7b\u578b', blank=True)),
            ],
            options={
                'db_table': 'alarm_log',
            },
        ),
        migrations.CreateModel(
            name='AlarmRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rule_name', models.CharField(max_length=100, null=True, verbose_name='\u89c4\u5219\u540d\u79f0', blank=True)),
                ('description', models.CharField(max_length=200, null=True, verbose_name='\u63cf\u8ff0', blank=True)),
                ('level', models.IntegerField(default=0, max_length=2, verbose_name='\u7b49\u7ea7')),
                ('status', models.IntegerField(default=-1, max_length=2, verbose_name='\u72b6\u6001')),
                ('sql', models.TextField(null=True, verbose_name='sql', blank=True)),
                ('time', models.IntegerField(default=-1, max_length=2, verbose_name='\u65f6\u95f4\u95f4\u9694\u72b6\u6001')),
                ('interval', models.IntegerField(default=0, max_length=10, verbose_name='\u65f6\u95f4\u95f4\u9694')),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'alarm_rule',
            },
        ),
        migrations.CreateModel(
            name='GroupRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=100, null=True, verbose_name='\u7ec4\u540d\u79f0', blank=True)),
                ('description', models.CharField(max_length=200, null=True, verbose_name='\u63cf\u8ff0', blank=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'group_rule',
            },
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('week', models.CharField(max_length=100, null=True, verbose_name='\u5de5\u4f5c\u65e5', blank=True)),
                ('state', models.CharField(max_length=100, null=True, verbose_name='\u4e0a\u73ed\u72b6\u6001 1-\u4e0a\u73ed 2-\u4f11\u606f', blank=True)),
                ('am_start_time', models.CharField(max_length=100, verbose_name='\u4e0a\u5348\u5f00\u59cb\u65f6\u95f4')),
                ('am_end_time', models.CharField(max_length=100, verbose_name='\u4e0a\u5348\u7ed3\u675f\u65f6\u95f4')),
                ('pm_start_time', models.CharField(max_length=100, verbose_name='\u4e0b\u5348\u5f00\u59cb\u65f6\u95f4')),
                ('pm_end_time', models.CharField(max_length=100, verbose_name='\u4e0b\u5348\u7ed3\u675f\u65f6\u95f4')),
            ],
            options={
                'db_table': 'work_day',
            },
        ),
        migrations.AddField(
            model_name='alarmrule',
            name='group',
            field=models.ForeignKey(blank=True, to='soc_knowledge.GroupRule', null=True),
        ),
        migrations.AddField(
            model_name='alarmlog',
            name='rule',
            field=models.ForeignKey(blank=True, to='soc_knowledge.AlarmRule', null=True),
        ),
    ]
