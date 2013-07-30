# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UDHscale.trail'
        db.add_column(u'muni_scales_udhscale', 'trail',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trails.Trail'], null=True),
                      keep_default=False)

        # Adding field 'UXCscale.trail'
        db.add_column(u'muni_scales_uxcscale', 'trail',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trails.Trail'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UDHscale.trail'
        db.delete_column(u'muni_scales_udhscale', 'trail_id')

        # Deleting field 'UXCscale.trail'
        db.delete_column(u'muni_scales_uxcscale', 'trail_id')


    models = {
        u'muni_scales.udhscale': {
            'Meta': {'object_name': 'UDHscale'},
            'average_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'average_slope': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'total_length': ('django.db.models.fields.IntegerField', [], {}),
            'trail': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trails.Trail']", 'null': 'True'})
        },
        u'muni_scales.uxcscale': {
            'Meta': {'object_name': 'UXCscale'},
            'average_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'maximum_slope_uh': ('django.db.models.fields.IntegerField', [], {}),
            'total_ascent': ('django.db.models.fields.IntegerField', [], {}),
            'total_length': ('django.db.models.fields.IntegerField', [], {}),
            'trail': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trails.Trail']", 'null': 'True'})
        },
        u'trails.trail': {
            'Meta': {'object_name': 'Trail'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'waypoints': ('django.contrib.gis.db.models.fields.LineStringField', [], {'dim': '3', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['muni_scales']