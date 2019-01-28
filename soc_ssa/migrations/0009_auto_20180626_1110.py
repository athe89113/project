# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0008_auto_20180625_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='secdatatag',
            name='diff_field',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='secdatatag',
            name='diff_value',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='seceventtype',
            name='type_desc',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='seceventtype',
            name='type_tag',
            field=models.ForeignKey(blank=True, to='soc_ssa.SECDataTag', null=True),
        ),
        migrations.AddField(
            model_name='secfieldmap',
            name='field_priority',
            field=models.IntegerField(default=0),
        ),
    ]
