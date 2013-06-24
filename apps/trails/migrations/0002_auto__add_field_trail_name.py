# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Trail.name'
        db.add_column(u'trails_trail', 'name',
                      self.gf('django.db.models.fields.CharField')(default='name', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Trail.name'
        db.delete_column(u'trails_trail', 'name')


    models = {
        u'trails.trail': {
            'Meta': {'object_name': 'Trail'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'trails.waypoint': {
            'Meta': {'object_name': 'WayPoint'},
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trail': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trails.Trail']"})
        }
    }

    complete_apps = ['trails']