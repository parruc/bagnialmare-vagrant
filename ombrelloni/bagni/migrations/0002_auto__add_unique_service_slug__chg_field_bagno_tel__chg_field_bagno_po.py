# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Service', fields ['slug']
        db.create_unique(u'bagni_service', ['slug'])


        # Changing field 'Bagno.tel'
        db.alter_column(u'bagni_bagno', 'tel', self.gf('django.db.models.fields.CharField')(max_length=75))

        # Changing field 'Bagno.point'
        db.alter_column(u'bagni_bagno', 'point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True))
        # Adding unique constraint on 'Bagno', fields ['slug']
        db.create_unique(u'bagni_bagno', ['slug'])


        # Changing field 'Bagno.number'
        db.alter_column(u'bagni_bagno', 'number', self.gf('django.db.models.fields.CharField')(max_length=15))

        # Changing field 'Bagno.site'
        db.alter_column(u'bagni_bagno', 'site', self.gf('django.db.models.fields.URLField')(max_length=75))

        # Changing field 'Bagno.mail'
        db.alter_column(u'bagni_bagno', 'mail', self.gf('django.db.models.fields.EmailField')(max_length=50))

    def backwards(self, orm):
        # Removing unique constraint on 'Bagno', fields ['slug']
        db.delete_unique(u'bagni_bagno', ['slug'])

        # Removing unique constraint on 'Service', fields ['slug']
        db.delete_unique(u'bagni_service', ['slug'])


        # Changing field 'Bagno.tel'
        db.alter_column(u'bagni_bagno', 'tel', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Bagno.point'
        db.alter_column(u'bagni_bagno', 'point', self.gf('django.contrib.gis.db.models.fields.PointField')(default=(0, 0)))

        # Changing field 'Bagno.number'
        db.alter_column(u'bagni_bagno', 'number', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Changing field 'Bagno.site'
        db.alter_column(u'bagni_bagno', 'site', self.gf('django.db.models.fields.URLField')(max_length=50))

        # Changing field 'Bagno.mail'
        db.alter_column(u'bagni_bagno', 'mail', self.gf('django.db.models.fields.CharField')(max_length=50))

    models = {
        u'bagni.bagno': {
            'Meta': {'object_name': 'Bagno'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bagni.Service']", 'symmetrical': 'False', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '75', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'})
        },
        u'bagni.service': {
            'Meta': {'object_name': 'Service'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'OT'", 'max_length': '50', 'blank': 'True'}),
            'free': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
        }
    }

    complete_apps = ['bagni']