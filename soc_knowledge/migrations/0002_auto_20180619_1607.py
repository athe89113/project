# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_knowledge', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KnowledgeStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('user', models.CharField(max_length=128, null=True, blank=True)),
                ('content', models.TextField()),
                ('relate', models.TextField(null=True, blank=True)),
                ('scene', models.CharField(default=b'', max_length=128)),
                ('description', models.CharField(max_length=2048, null=True, blank=True)),
                ('operate', models.CharField(max_length=2048, null=True, blank=True)),
                ('decide', models.CharField(max_length=2048, null=True, blank=True)),
                ('feedback', models.CharField(max_length=2048, null=True, blank=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('search_letter', models.CharField(max_length=10, null=True, blank=True)),
            ],
            options={
                'db_table': 'knowledge_store',
                'verbose_name': '\u77e5\u8bc6\u5e93',
            },
        ),
        migrations.CreateModel(
            name='KnowledgeTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'knowledge_tag',
                'verbose_name': '\u77e5\u8bc6\u70b9\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='KnowledgeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'knowledge_type',
                'verbose_name': '\u77e5\u8bc6\u70b9\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='PlanContacts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'plan_contacts',
                'verbose_name': '\u9884\u6848\u8054\u7cfb\u4eba',
            },
        ),
        migrations.CreateModel(
            name='PlanStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('user', models.CharField(max_length=128, null=True, blank=True)),
                ('level', models.SmallIntegerField()),
                ('scene', models.CharField(default=b'', max_length=128)),
                ('brief', models.CharField(max_length=2048, null=True, blank=True)),
                ('description', models.TextField()),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'plan_store',
                'verbose_name': '\u9884\u6848\u5e93',
            },
        ),
        migrations.CreateModel(
            name='PlanTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'plan_tag',
                'verbose_name': '\u9884\u6848\u6807\u7b7e',
            },
        ),
        migrations.CreateModel(
            name='PlanType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'plan_type',
                'verbose_name': '\u9884\u6848\u7c7b\u578b',
            },
        ),
        migrations.CreateModel(
            name='SceneType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'scene_type',
                'verbose_name': '\u5e94\u7528\u573a\u666f',
            },
        ),
        migrations.CreateModel(
            name='SearchKnowledgeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('search_type', models.CharField(max_length=20, null=True, blank=True)),
                ('result_id', models.IntegerField()),
                ('search_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'search_knowledge_log',
                'verbose_name': '\u67e5\u8be2\u5e93\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='VulStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vul_name', models.CharField(max_length=128, null=True, blank=True)),
                ('cve_id', models.CharField(max_length=128, null=True, blank=True)),
                ('vul_id', models.CharField(max_length=128, unique=True, null=True, blank=True)),
                ('vul_level', models.CharField(max_length=10, null=True, blank=True)),
                ('vul_type', models.CharField(max_length=128, null=True, blank=True)),
                ('attack_type', models.CharField(max_length=128, null=True, blank=True)),
                ('impact', models.CharField(max_length=2048, null=True, blank=True)),
                ('description', models.CharField(max_length=2048, null=True, blank=True)),
                ('vul_source', models.CharField(max_length=128, null=True, blank=True)),
                ('advice', models.CharField(max_length=2048, null=True, blank=True)),
                ('patch', models.CharField(max_length=1024, null=True, blank=True)),
                ('reference', models.CharField(max_length=2048, null=True, blank=True)),
                ('publish_date', models.DateField(null=True, blank=True)),
                ('update_date', models.DateField(null=True, blank=True)),
                ('data_source', models.CharField(max_length=10, null=True, blank=True)),
                ('tag', models.CharField(max_length=128, null=True, blank=True)),
                ('firm', models.CharField(max_length=128, null=True, blank=True)),
                ('score', models.CharField(max_length=10, null=True, blank=True)),
                ('cvss', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
                'db_table': 'vul_store',
                'verbose_name': '\u6f0f\u6d1e\u5e93',
            },
        ),
        migrations.CreateModel(
            name='VulStoreVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_date', models.CharField(default=b'', max_length=30)),
                ('last_version', models.CharField(default=b'', max_length=30)),
                ('version', models.CharField(default=b'', max_length=30)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'vul_store_version',
                'verbose_name': '\u6f0f\u6d1e\u5e93\u7248\u672c',
            },
        ),
        migrations.AddField(
            model_name='planstore',
            name='tag',
            field=models.ManyToManyField(to='soc_knowledge.PlanTag', db_table=b'plan_store_tag'),
        ),
        migrations.AddField(
            model_name='planstore',
            name='type',
            field=models.ForeignKey(blank=True, to='soc_knowledge.PlanType', null=True),
        ),
        migrations.AddField(
            model_name='plancontacts',
            name='plan',
            field=models.ForeignKey(blank=True, to='soc_knowledge.PlanStore', null=True),
        ),
        migrations.AddField(
            model_name='knowledgestore',
            name='tag',
            field=models.ManyToManyField(to='soc_knowledge.KnowledgeTag', db_table=b'knowledge_store_tag'),
        ),
        migrations.AddField(
            model_name='knowledgestore',
            name='type',
            field=models.ForeignKey(to='soc_knowledge.KnowledgeType'),
        ),
    ]
