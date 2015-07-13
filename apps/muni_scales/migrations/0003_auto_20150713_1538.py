# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muni_scales', '0002_auto_20150613_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='udhscale',
            name='trail',
            field=models.OneToOneField(default=1, blank=True, to='trails.Trail'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uxcscale',
            name='trail',
            field=models.OneToOneField(default=1, blank=True, to='trails.Trail'),
            preserve_default=False,
        ),
    ]
