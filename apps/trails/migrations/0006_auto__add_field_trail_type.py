# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Trail.type'
        db.add_column(u'trails_trail', 'type',
                      self.gf('django.db.models.fields.CharField')(default='unknown', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Trail.type'
        db.delete_column(u'trails_trail', 'type')


    models = {
        u'trails.trail': {
            'Meta': {'object_name': 'Trail'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'waypoints': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'dim': '3', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['trails']