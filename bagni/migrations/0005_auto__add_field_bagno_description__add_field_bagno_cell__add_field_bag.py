# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Bagno.description'
        db.add_column(u'bagni_bagno', 'description',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=500),
                      keep_default=False)

        # Adding field 'Bagno.cell'
        db.add_column(u'bagni_bagno', 'cell',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=75, blank=True),
                      keep_default=False)

        # Adding field 'Bagno.winter_tel'
        db.add_column(u'bagni_bagno', 'winter_tel',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=75, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Bagno.description'
        db.delete_column(u'bagni_bagno', 'description')

        # Deleting field 'Bagno.cell'
        db.delete_column(u'bagni_bagno', 'cell')

        # Deleting field 'Bagno.winter_tel'
        db.delete_column(u'bagni_bagno', 'winter_tel')


    models = {
        u'bagni.bagno': {
            'Meta': {'object_name': 'Bagno'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bagni.Service']", 'symmetrical': 'False', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '75', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'winter_tel': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'})
        },
        u'bagni.image': {
            'Meta': {'object_name': 'Image'},
            'bagno': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bagni.Bagno']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'})
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