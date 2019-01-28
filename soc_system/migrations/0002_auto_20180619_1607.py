# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('soc', '0002_auto_20180619_1607'),
        ('soc_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancedMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'default', max_length=10)),
                ('name', models.CharField(max_length=24)),
                ('sort', models.PositiveSmallIntegerField(default=50)),
                ('is_landing', models.PositiveSmallIntegerField(default=0)),
                ('enable', models.PositiveSmallIntegerField(default=1)),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'advanced_menu',
                'verbose_name': '\u81ea\u5b9a\u4e49\u83dc\u5355',
            },
        ),
        migrations.CreateModel(
            name='BlackIPList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_black', models.IntegerField(default=1, choices=[(1, b'\xe9\xbb\x91\xe5\x90\x8d\xe5\x8d\x95'), (2, b'\xe7\x99\xbd\xe5\x90\x8d\xe5\x8d\x95')])),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('ip', models.CharField(max_length=64)),
                ('type', models.IntegerField(default=0)),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'black_ip_list',
            },
        ),
        migrations.CreateModel(
            name='DefaultMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('index', models.PositiveIntegerField()),
                ('sort', models.PositiveSmallIntegerField(default=50)),
                ('level', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=32)),
                ('topic', models.CharField(max_length=32)),
                ('is_landing', models.PositiveSmallIntegerField(default=0)),
                ('enable', models.PositiveSmallIntegerField(default=1)),
                ('company_show', models.IntegerField(default=1)),
                ('parent', models.ForeignKey(to='soc_system.DefaultMenu', null=True)),
            ],
            options={
                'db_table': 'default_menu',
                'verbose_name': '\u9ed8\u8ba4\u83dc\u5355',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(choices=[(1, b'SMTP\xe9\x82\xae\xe4\xbb\xb6'), (2, b'\xe7\x9f\xad\xe4\xbf\xa1'), (4, b'cloud\xe9\x82\xae\xe4\xbb\xb6')])),
                ('smtp_server', models.CharField(max_length=128, blank=True)),
                ('send_sender', models.CharField(max_length=64, blank=True)),
                ('user', models.CharField(max_length=64, blank=True)),
                ('password', models.CharField(max_length=64, blank=True)),
                ('tls_or_ssl', models.BooleanField(default=False)),
                ('api', models.CharField(max_length=256, blank=True)),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'system_message',
                'verbose_name': '\u6d88\u606f\u4e2d\u5fc3\u8bbe\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('uuid', models.CharField(default=uuid.uuid4, max_length=200, null=True, blank=True)),
                ('ip', models.CharField(default=b'127.0.0.1', max_length=200)),
                ('port', models.IntegerField(default=80)),
                ('role', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=15)),
                ('auth_key', models.TextField(null=True)),
                ('status', models.PositiveSmallIntegerField(default=0)),
                ('api_url', models.CharField(max_length=256, null=True, blank=True)),
                ('secret_id', models.CharField(max_length=64, null=True)),
                ('secret_key', models.CharField(max_length=128, null=True)),
                ('accept_parent_connection', models.PositiveSmallIntegerField(default=0)),
                ('accept_next_settings', models.TextField(default=b'{}')),
                ('accept_apply_message', models.PositiveSmallIntegerField(default=0)),
                ('accept_apply_loophole', models.PositiveSmallIntegerField(default=0)),
                ('accept_apply_policy', models.PositiveSmallIntegerField(default=0)),
                ('accept_apply_event_db', models.PositiveSmallIntegerField(default=0)),
                ('accept_apply_engine', models.PositiveSmallIntegerField(default=0)),
                ('accept_apply_center', models.PositiveSmallIntegerField(default=0)),
                ('notify_when_lose_children', models.PositiveSmallIntegerField(default=1)),
                ('last_heartbeat', models.DateTimeField(auto_now_add=True, null=True)),
                ('next_check', models.DateTimeField(auto_now_add=True, null=True)),
                ('version', models.CharField(default=b'', max_length=10, null=True)),
                ('info', models.CharField(default=b'', max_length=256, null=True, blank=True)),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'system_node',
                'verbose_name': '\u7ea7\u8054\u8282\u70b9',
            },
        ),
        migrations.CreateModel(
            name='SetPay',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bank', models.CharField(max_length=32, blank=True)),
                ('username', models.CharField(max_length=32, blank=True)),
                ('bank_user', models.CharField(max_length=64, blank=True)),
                ('email', models.CharField(max_length=32, blank=True)),
                ('pay_online', models.BooleanField(default=True)),
                ('pay_outline', models.BooleanField(default=True)),
                ('invoice', models.BooleanField(default=True)),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'system_setpay',
                'verbose_name': '\u8d22\u52a1\u8bbe\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='SystemUpgradeFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('u_type', models.CharField(max_length=15)),
                ('upgrade_type', models.CharField(max_length=15)),
                ('version', models.CharField(max_length=15)),
                ('path', models.FilePathField(null=True)),
                ('build_date', models.DateTimeField(null=True, blank=True)),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'system_upgrade_file',
                'verbose_name': '\u5347\u7ea7\u6587\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='SystemUpgradeTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('u_type', models.CharField(max_length=15)),
                ('target_id', models.IntegerField(null=True)),
                ('target_name', models.CharField(max_length=256)),
                ('target_uuid', models.CharField(max_length=256)),
                ('target_version', models.CharField(max_length=15)),
                ('target_parent_id', models.IntegerField(null=True)),
                ('file_uuid', models.CharField(max_length=256)),
                ('file_version', models.CharField(max_length=15)),
                ('status', models.PositiveSmallIntegerField(default=0)),
                ('percent', models.PositiveSmallIntegerField(default=0)),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'system_upgrade_task',
                'verbose_name': '\u5347\u7ea7\u4efb\u52a1',
            },
        ),
        migrations.AddField(
            model_name='advancedmenu',
            name='default_menu',
            field=models.ForeignKey(to='soc_system.DefaultMenu', null=True),
        ),
    ]
