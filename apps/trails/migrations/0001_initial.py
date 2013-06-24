# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Trail'
        db.create_table(u'trails_trail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
            ('edited', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'trails', ['Trail'])

        # Adding model 'WayPoint'
        db.create_table(u'trails_waypoint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('trail', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trails.Trail'])),
        ))
        db.send_create_signal(u'trails', ['WayPoint'])


    def backwards(self, orm):
        # Deleting model 'Trail'
        db.delete_table(u'trails_trail')

        # Deleting model 'WayPoint'
        db.delete_table(u'trails_waypoint')


    models = {
        u'trails.trail': {
            'Meta': {'object_name': 'Trail'},
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'trails.waypoint': {
            'Meta': {'object_name': 'WayPoint'},
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trail': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trails.Trail']"})
        }
    }

    complete_apps = ['trails']