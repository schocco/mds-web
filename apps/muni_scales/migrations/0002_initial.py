# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UDHscale'
        db.create_table(u'muni_scales_udhscale', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_length', self.gf('django.db.models.fields.IntegerField')()),
            ('maximum_difficulty', self.gf('apps.muni_scales.fields.MscaleField')(max_digits=2, decimal_places=1)),
            ('average_difficulty', self.gf('apps.muni_scales.fields.MscaleField')(max_digits=2, decimal_places=1)),
            ('average_slope', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'muni_scales', ['UDHscale'])

        # Adding model 'UXCscale'
        db.create_table(u'muni_scales_uxcscale', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('total_length', self.gf('django.db.models.fields.IntegerField')()),
            ('maximum_difficulty', self.gf('apps.muni_scales.fields.MscaleField')(max_digits=2, decimal_places=1)),
            ('average_difficulty', self.gf('apps.muni_scales.fields.MscaleField')(max_digits=2, decimal_places=1)),
            ('total_ascent', self.gf('django.db.models.fields.IntegerField')()),
            ('maximum_slope_uh', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'muni_scales', ['UXCscale'])


    def backwards(self, orm):
        # Deleting model 'UDHscale'
        db.delete_table(u'muni_scales_udhscale')

        # Deleting model 'UXCscale'
        db.delete_table(u'muni_scales_uxcscale')


    models = {
        u'muni_scales.udhscale': {
            'Meta': {'object_name': 'UDHscale'},
            'average_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'average_slope': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'total_length': ('django.db.models.fields.IntegerField', [], {})
        },
        u'muni_scales.uxcscale': {
            'Meta': {'object_name': 'UXCscale'},
            'average_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'maximum_slope_uh': ('django.db.models.fields.IntegerField', [], {}),
            'total_ascent': ('django.db.models.fields.IntegerField', [], {}),
            'total_length': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['muni_scales']