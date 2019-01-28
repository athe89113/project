# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0002_auto_20180619_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ssareportresult',
            name='path',
        ),
        migrations.RemoveField(
            model_name='ssareportresult',
            name='size',
        ),
        migrations.AddField(
            model_name='ssareportresult',
            name='docx_path',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='ssareportresult',
            name='docx_size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='ssareportresult',
            name='pdf_path',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='ssareportresult',
            name='pdf_size',
            field=models.IntegerField(default=0),
        ),
    ]
