# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0005_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssareporttemplate',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
