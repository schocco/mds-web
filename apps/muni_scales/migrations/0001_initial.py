# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.muni_scales.fields


class Migration(migrations.Migration):

    dependencies = [
        ('trails', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UDHscale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_length', models.IntegerField(help_text='Total trail length in meters', verbose_name='total length')),
                ('maximum_difficulty', apps.muni_scales.fields.MscaleField(help_text='Maximum difficulty on the M-Scale', verbose_name='maximum difficulty', max_digits=2, decimal_places=1)),
                ('average_difficulty', apps.muni_scales.fields.MscaleField(help_text='average difficulty on the M-Scale', verbose_name='average difficulty', max_digits=2, decimal_places=1)),
                ('average_slope', models.IntegerField(help_text='average slope in %', verbose_name='average slope')),
                ('trail', models.OneToOneField(null=True, blank=True, to='trails.Trail')),
            ],
            options={
                'verbose_name': 'UDH Scale Entity',
                'verbose_name_plural': 'UDH Scale Entities',
            },
        ),
        migrations.CreateModel(
            name='UXCscale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_length', models.IntegerField(help_text='Total trail length in meters', verbose_name='total length')),
                ('maximum_difficulty', apps.muni_scales.fields.MscaleField(help_text='Maximum difficulty on the M-Scale', verbose_name='maximum difficulty', max_digits=2, decimal_places=1)),
                ('average_difficulty', apps.muni_scales.fields.MscaleField(help_text='average difficulty on the M-Scale', verbose_name='average difficulty', max_digits=2, decimal_places=1)),
                ('total_ascent', models.IntegerField(help_text='total ascent in meters', verbose_name='total ascent')),
                ('maximum_slope_uh', models.IntegerField(help_text='slope in % of the steepest uphill section', verbose_name='maximum slope (uphill)')),
                ('trail', models.OneToOneField(null=True, blank=True, to='trails.Trail')),
            ],
            options={
                'verbose_name': 'UXC Scale Entity',
                'verbose_name_plural': 'UXC Scale Entities',
            },
        ),
    ]
