# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soc_ssa', '0012_auto_20180626_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='ssareporttemplate',
            name='template_type',
            field=models.IntegerField(default=1),
        ),
    ]
