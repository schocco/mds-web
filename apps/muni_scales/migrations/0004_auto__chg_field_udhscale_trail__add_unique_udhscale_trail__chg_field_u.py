# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'UDHscale.trail'
        db.alter_column(u'muni_scales_udhscale', 'trail_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['trails.Trail'], unique=True, null=True))
        # Adding unique constraint on 'UDHscale', fields ['trail']
        db.create_unique(u'muni_scales_udhscale', ['trail_id'])


        # Changing field 'UXCscale.trail'
        db.alter_column(u'muni_scales_uxcscale', 'trail_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['trails.Trail'], unique=True, null=True))
        # Adding unique constraint on 'UXCscale', fields ['trail']
        db.create_unique(u'muni_scales_uxcscale', ['trail_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'UXCscale', fields ['trail']
        db.delete_unique(u'muni_scales_uxcscale', ['trail_id'])

        # Removing unique constraint on 'UDHscale', fields ['trail']
        db.delete_unique(u'muni_scales_udhscale', ['trail_id'])


        # Changing field 'UDHscale.trail'
        db.alter_column(u'muni_scales_udhscale', 'trail_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trails.Trail'], null=True))

        # Changing field 'UXCscale.trail'
        db.alter_column(u'muni_scales_uxcscale', 'trail_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trails.Trail'], null=True))

    models = {
        u'muni_scales.udhscale': {
            'Meta': {'object_name': 'UDHscale'},
            'average_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'average_slope': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'total_length': ('django.db.models.fields.IntegerField', [], {}),
            'trail': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['trails.Trail']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'muni_scales.uxcscale': {
            'Meta': {'object_name': 'UXCscale'},
            'average_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_difficulty': ('apps.muni_scales.fields.MscaleField', [], {'max_digits': '2', 'decimal_places': '1'}),
            'maximum_slope_uh': ('django.db.models.fields.IntegerField', [], {}),
            'total_ascent': ('django.db.models.fields.IntegerField', [], {}),
            'total_length': ('django.db.models.fields.IntegerField', [], {}),
            'trail': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['trails.Trail']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'trails.trail': {
            'Meta': {'object_name': 'Trail'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'waypoints': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'dim': '3', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['muni_scales']