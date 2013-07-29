# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'WayPoint'
        db.delete_table(u'trails_waypoint')

        # Adding field 'Trail.waypoints'
        db.add_column(u'trails_trail', 'waypoints',
                      self.gf('django.contrib.gis.db.models.fields.LineStringField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'WayPoint'
        db.create_table(u'trails_waypoint', (
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('trail', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trails.Trail'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'trails', ['WayPoint'])

        # Deleting field 'Trail.waypoints'
        db.delete_column(u'trails_trail', 'waypoints')


    models = {
        u'trails.trail': {
            'Meta': {'object_name': 'Trail'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'waypoints': ('django.contrib.gis.db.models.fields.LineStringField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['trails']