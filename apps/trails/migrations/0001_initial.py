# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('type', models.CharField(max_length=100, verbose_name='trail type', choices=[(b'unknown', 'unknown'), (b'uphill', 'uphill'), (b'downhill', 'downhill'), (b'xc', 'cross country')])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('edited', models.DateTimeField(auto_now=True, verbose_name='last change')),
                ('description', models.CharField(max_length=500, verbose_name='description', blank=True)),
                ('waypoints', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326, dim=3, verbose_name='waypoints')),
                ('trail_length', models.IntegerField(help_text='in meters', null=True, verbose_name='length', blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
