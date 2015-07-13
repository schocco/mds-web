# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('muni_scales', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='udhscale',
            old_name='average_difficulty',
            new_name='avg_difficulty',
        ),
        migrations.RenameField(
            model_name='udhscale',
            old_name='average_slope',
            new_name='avg_slope',
        ),
        migrations.RenameField(
            model_name='udhscale',
            old_name='maximum_difficulty',
            new_name='max_difficulty',
        ),
        migrations.RenameField(
            model_name='uxcscale',
            old_name='average_difficulty',
            new_name='avg_difficulty',
        ),
        migrations.RenameField(
            model_name='uxcscale',
            old_name='maximum_difficulty',
            new_name='max_difficulty',
        ),
        migrations.RenameField(
            model_name='uxcscale',
            old_name='maximum_slope_uh',
            new_name='max_slope_uh',
        ),
    ]
