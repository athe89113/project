# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('soc', '0002_auto_20180619_1607'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('soc_ssa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelfServiceConf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service', models.CharField(max_length=256)),
                ('host', models.CharField(max_length=256)),
                ('username', models.CharField(max_length=256, null=True, blank=True)),
                ('password', models.CharField(max_length=256, null=True, blank=True)),
                ('agent', models.ForeignKey(blank=True, to='soc.Agent', null=True)),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
            ],
            options={
                'db_table': 'ssa_self_service_conf',
                'verbose_name': '\u5927\u6570\u636e\u670d\u52a1\u914d\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='SSAAlarmCell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=125)),
                ('key', models.CharField(max_length=256)),
                ('conf_type', models.IntegerField()),
                ('warning', models.IntegerField()),
                ('alarm', models.IntegerField()),
                ('unit', models.CharField(max_length=125, null=True, blank=True)),
                ('expression', models.CharField(default=b'>=', max_length=125)),
                ('message', models.CharField(max_length=256, null=True, blank=True)),
            ],
            options={
                'db_table': 'ssa_alarm_cell',
                'verbose_name': '\u6001\u52bf\u611f\u77e5-\u9884\u8b66/\u544a\u8b66\u9879',
            },
        ),
        migrations.CreateModel(
            name='SSAAlarmConf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_alarm_count', models.IntegerField(default=3)),
                ('toggle_condition', models.IntegerField(default=1)),
                ('conf_type', models.IntegerField()),
                ('agent', models.ForeignKey(to='soc.Agent')),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
            ],
            options={
                'db_table': 'ssa_alarm_conf',
                'verbose_name': '\u6001\u52bf\u611f\u77e5-\u9884\u8b66/\u544a\u8b66\u914d\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='SSAAlarmConfCell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enable', models.IntegerField(default=0)),
                ('warning', models.IntegerField()),
                ('alarm', models.IntegerField()),
                ('agent', models.ForeignKey(to='soc.Agent')),
                ('cell', models.ForeignKey(to='soc_ssa.SSAAlarmCell')),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
            ],
            options={
                'db_table': 'ssa_alarm_conf_cell',
                'verbose_name': '\u6001\u52bf\u611f\u77e5-\u9884\u8b66/\u544a\u8b66\u9879\u914d\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='SSAAlarmNotifyConf',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('conf_type', models.IntegerField()),
                ('email', models.IntegerField(default=0)),
                ('sms', models.IntegerField(default=0)),
                ('agent', models.ForeignKey(to='soc.Agent')),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ssa_alarm_notify_conf',
                'verbose_name': '\u6001\u52bf\u611f\u77e5-\u9884\u8b66/\u544a\u8b66\u9879\u914d\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='SSAChart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('type', models.CharField(max_length=256)),
                ('chart_type', models.CharField(max_length=256)),
                ('map_type', models.CharField(max_length=256, null=True, blank=True)),
                ('query_time', models.IntegerField(default=1)),
                ('styles', models.TextField(null=True)),
                ('x', models.TextField(null=True)),
                ('y', models.TextField(null=True)),
                ('limit', models.IntegerField(default=0)),
                ('cache', models.TextField(null=True)),
                ('description', models.CharField(max_length=256)),
                ('remark', models.CharField(max_length=256)),
                ('agent', models.ForeignKey(blank=True, to='soc.Agent', null=True)),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
            ],
            options={
                'db_table': 'ssa_chart',
                'verbose_name': '\u6001\u52bf\u611f\u77e5-\u56fe\u8868',
            },
        ),
        migrations.CreateModel(
            name='SSADashBorad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('type', models.CharField(max_length=256)),
                ('query_time', models.IntegerField(default=1)),
                ('agent', models.ForeignKey(blank=True, to='soc.Agent', null=True)),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
            ],
            options={
                'db_table': 'ssa_dashboard',
                'verbose_name': '\u6001\u52bf\u611f\u77e5-DashBorad',
            },
        ),
        migrations.CreateModel(
            name='SSADashBoradCell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField(default=0)),
                ('agent', models.ForeignKey(blank=True, to='soc.Agent', null=True)),
                ('chart', models.ForeignKey(to='soc_ssa.SSAChart')),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
                ('dashboard', models.ForeignKey(to='soc_ssa.SSADashBorad')),
            ],
            options={
                'db_table': 'ssa_dashboard_cell',
                'verbose_name': '\u6001\u52bf\u611f\u77e5-DashBorad\u5143\u7d20',
            },
        ),
        migrations.CreateModel(
            name='SSADataTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('path', models.CharField(max_length=256)),
                ('time_format', models.CharField(default=b'yyyy-MM-dd-HH', max_length=256)),
                ('agent', models.ForeignKey(blank=True, to='soc.Agent', null=True)),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
            ],
            options={
                'db_table': 'ssa_data_tag',
                'verbose_name': '\u6570\u636e\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='SSAFieldMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=256)),
                ('precedence', models.IntegerField(default=0)),
                ('items', models.TextField(default=b'[]')),
                ('data_tag', models.ForeignKey(blank=True, to='soc_ssa.SSADataTag', null=True)),
            ],
            options={
                'db_table': 'ssa_field_map',
            },
        ),
        migrations.CreateModel(
            name='SSAReportCell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('data_key', models.CharField(max_length=256)),
                ('data_type', models.IntegerField(default=1)),
                ('default_chart', models.CharField(default=b'pie', max_length=256)),
                ('description', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'ssa_report_cell',
                'verbose_name': '\u62a5\u8868\u6a21\u677f\u5143\u7d20',
            },
        ),
        migrations.CreateModel(
            name='SSAReportResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('path', models.CharField(max_length=256)),
                ('size', models.IntegerField()),
                ('agent', models.ForeignKey(blank=True, to='soc.Agent', null=True)),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
            ],
            options={
                'db_table': 'ssa_report_result',
                'verbose_name': '\u62a5\u8868',
            },
        ),
        migrations.CreateModel(
            name='SSAReportTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('schedule_type', models.PositiveSmallIntegerField()),
                ('schedule_start_date', models.DateField(null=True)),
                ('schedule_days', models.PositiveSmallIntegerField()),
                ('schedule_months', models.PositiveSmallIntegerField(default=1)),
                ('schedule_time', models.TimeField(null=True)),
                ('next_scan_time', models.DateTimeField(null=True)),
                ('agent', models.ForeignKey(blank=True, to='soc.Agent', null=True)),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
            ],
            options={
                'db_table': 'ssa_report_template',
                'verbose_name': '\u62a5\u8868\u6a21\u677f',
            },
        ),
        migrations.CreateModel(
            name='SSAReportTemplateCell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cycle', models.IntegerField()),
                ('has_table', models.IntegerField(default=0)),
                ('chart_type', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('remark', models.CharField(max_length=256)),
                ('order', models.IntegerField()),
                ('agent', models.ForeignKey(blank=True, to='soc.Agent', null=True)),
                ('cell', models.ForeignKey(blank=True, to='soc_ssa.SSAReportCell', null=True)),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
                ('template', models.ForeignKey(to='soc_ssa.SSAReportTemplate', null=True)),
            ],
            options={
                'db_table': 'ssa_report_template_cell',
                'verbose_name': '\u62a5\u8868\u6a21\u677f\u5143\u7d20',
            },
        ),
        migrations.CreateModel(
            name='SSARuleManage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('type', models.IntegerField(default=1)),
                ('sql', models.CharField(max_length=1024)),
                ('agent', models.ForeignKey(blank=True, to='soc.Agent', null=True)),
                ('company', models.ForeignKey(blank=True, to='soc.Company', null=True)),
                ('parent', models.ForeignKey(related_name='parent_folder', verbose_name='\u7236\u76ee\u5f55', to='soc_ssa.SSARuleManage', null=True)),
            ],
            options={
                'db_table': 'ssa_rule_manage',
                'verbose_name': '\u4e13\u5bb6\u5206\u6790\u7cfb\u7edf',
            },
        ),
        migrations.CreateModel(
            name='SSAScoreSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('security_mark', models.IntegerField(default=0)),
                ('hole_assets', models.IntegerField(default=0)),
                ('hole_serious', models.IntegerField(default=0)),
                ('attack', models.IntegerField(default=0)),
                ('trojan', models.IntegerField(default=0)),
                ('business_health', models.IntegerField(default=0)),
                ('business_visit', models.IntegerField(default=0)),
                ('score_date', models.DateField()),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'ssa_score_system',
                'verbose_name': '\u6001\u52bf\u611f\u77e5\u8bc4\u5206\u7cfb\u7edf',
            },
        ),
        migrations.AddField(
            model_name='ssareportresult',
            name='template',
            field=models.ForeignKey(to='soc_ssa.SSAReportTemplate', null=True),
        ),
        migrations.AddField(
            model_name='ssachart',
            name='data_tag',
            field=models.ForeignKey(to='soc_ssa.SSADataTag'),
        ),
    ]
