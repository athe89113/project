# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import soc_user.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('soc', '0002_auto_20180619_1607'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('soc_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('default_enable', models.IntegerField(default=1)),
                ('parent', models.ForeignKey(blank=True, to='soc_user.Permissions', null=True)),
            ],
            options={
                'db_table': 'permissions',
            },
        ),
        migrations.CreateModel(
            name='PermissionUrls',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=256)),
                ('method', models.CharField(default=b'GET', max_length=125)),
                ('permissions', models.ForeignKey(to='soc_user.Permissions')),
            ],
            options={
                'db_table': 'permission_urls',
            },
        ),
        migrations.CreateModel(
            name='RolePermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enable', models.IntegerField(default=1)),
                ('agent', models.ForeignKey(to='soc.Agent')),
                ('permissions', models.ForeignKey(to='soc_user.Permissions')),
            ],
            options={
                'db_table': 'role_permissions',
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('enable', models.IntegerField(default=1)),
                ('is_admin', models.IntegerField(default=0)),
                ('two_factor', models.IntegerField(default=0)),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'roles',
            },
        ),
        migrations.CreateModel(
            name='SecretKey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=128)),
                ('enable', models.IntegerField(default=0)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('last_used', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=11, null=True)),
                ('gs_status', models.IntegerField(default=0)),
                ('google_secret', models.CharField(max_length=30)),
                ('is_locked', models.IntegerField(default=0)),
                ('role_type', models.IntegerField()),
                ('avatar', models.ImageField(default=b'images/default_avatar.jpg', null=True, upload_to=soc_user.models._user_directory_path, blank=True)),
                ('last_login_ip', models.GenericIPAddressField(null=True)),
                ('is_admin', models.PositiveSmallIntegerField(default=0)),
                ('key', models.CharField(default=uuid.uuid4, max_length=64)),
                ('fail_count', models.IntegerField(default=10)),
                ('fail_range_time', models.IntegerField(default=180)),
                ('fail_ban_time', models.IntegerField(default=3600)),
                ('fail_self_uban', models.IntegerField(default=0)),
                ('is_ghost', models.IntegerField(default=0)),
                ('ip', models.CharField(default=b'', max_length=64, null=True)),
                ('employee_id', models.CharField(max_length=64, null=True, blank=True)),
                ('agent', models.ForeignKey(to='soc.Agent')),
                ('company', models.ForeignKey(to='soc.Company', null=True)),
                ('roles', models.ManyToManyField(to='soc_user.Roles')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VerifyTmp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.PositiveSmallIntegerField(default=1)),
                ('email', models.EmailField(max_length=128)),
                ('phone', models.CharField(default=b'', max_length=11)),
                ('link_code', models.CharField(default=b'', max_length=256, null=True, blank=True)),
                ('captcha', models.CharField(default=b'', max_length=64, null=True, blank=True)),
                ('expire_time', models.DateTimeField()),
                ('validated', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'db_table': 'verify_tmp',
            },
        ),
        migrations.CreateModel(
            name='WorkGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('agent', models.ForeignKey(to='soc.Agent')),
            ],
            options={
                'db_table': 'work_group',
            },
        ),
        migrations.AddField(
            model_name='userinfo',
            name='work_group',
            field=models.ForeignKey(to='soc_user.WorkGroup', null=True),
        ),
        migrations.AddField(
            model_name='secretkey',
            name='user',
            field=models.ForeignKey(to='soc_user.UserInfo'),
        ),
        migrations.AddField(
            model_name='rolepermissions',
            name='role',
            field=models.ForeignKey(to='soc_user.Roles'),
        ),
        migrations.AlterUniqueTogether(
            name='workgroup',
            unique_together=set([('name', 'agent')]),
        ),
    ]
