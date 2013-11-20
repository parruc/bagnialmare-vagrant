# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Bagno.name_en'
        db.add_column(u'bagni_bagno', 'name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bagno.name_it'
        db.add_column(u'bagni_bagno', 'name_it',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bagno.description_en'
        db.add_column(u'bagni_bagno', 'description_en',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bagno.description_it'
        db.add_column(u'bagni_bagno', 'description_it',
                      self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bagno.slug_en'
        db.add_column(u'bagni_bagno', 'slug_en',
                      self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bagno.slug_it'
        db.add_column(u'bagni_bagno', 'slug_it',
                      self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bagno.address_en'
        db.add_column(u'bagni_bagno', 'address_en',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bagno.address_it'
        db.add_column(u'bagni_bagno', 'address_it',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bagno.city_en'
        db.add_column(u'bagni_bagno', 'city_en',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Bagno.city_it'
        db.add_column(u'bagni_bagno', 'city_it',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Bagno.number'
        db.alter_column(u'bagni_bagno', 'number', self.gf('django.db.models.fields.CharField')(max_length=30))
        # Adding field 'Service.name_en'
        db.add_column(u'bagni_service', 'name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Service.name_it'
        db.add_column(u'bagni_service', 'name_it',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Service.slug_en'
        db.add_column(u'bagni_service', 'slug_en',
                      self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Service.slug_it'
        db.add_column(u'bagni_service', 'slug_it',
                      self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Image.name_en'
        db.add_column(u'bagni_image', 'name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Image.name_it'
        db.add_column(u'bagni_image', 'name_it',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Image.slug_en'
        db.add_column(u'bagni_image', 'slug_en',
                      self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Image.slug_it'
        db.add_column(u'bagni_image', 'slug_it',
                      self.gf('autoslug.fields.AutoSlugField')(max_length=50, unique=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Bagno.name_en'
        db.delete_column(u'bagni_bagno', 'name_en')

        # Deleting field 'Bagno.name_it'
        db.delete_column(u'bagni_bagno', 'name_it')

        # Deleting field 'Bagno.description_en'
        db.delete_column(u'bagni_bagno', 'description_en')

        # Deleting field 'Bagno.description_it'
        db.delete_column(u'bagni_bagno', 'description_it')

        # Deleting field 'Bagno.slug_en'
        db.delete_column(u'bagni_bagno', 'slug_en')

        # Deleting field 'Bagno.slug_it'
        db.delete_column(u'bagni_bagno', 'slug_it')

        # Deleting field 'Bagno.address_en'
        db.delete_column(u'bagni_bagno', 'address_en')

        # Deleting field 'Bagno.address_it'
        db.delete_column(u'bagni_bagno', 'address_it')

        # Deleting field 'Bagno.city_en'
        db.delete_column(u'bagni_bagno', 'city_en')

        # Deleting field 'Bagno.city_it'
        db.delete_column(u'bagni_bagno', 'city_it')


        # Changing field 'Bagno.number'
        db.alter_column(u'bagni_bagno', 'number', self.gf('django.db.models.fields.CharField')(max_length=15))
        # Deleting field 'Service.name_en'
        db.delete_column(u'bagni_service', 'name_en')

        # Deleting field 'Service.name_it'
        db.delete_column(u'bagni_service', 'name_it')

        # Deleting field 'Service.slug_en'
        db.delete_column(u'bagni_service', 'slug_en')

        # Deleting field 'Service.slug_it'
        db.delete_column(u'bagni_service', 'slug_it')

        # Deleting field 'Image.name_en'
        db.delete_column(u'bagni_image', 'name_en')

        # Deleting field 'Image.name_it'
        db.delete_column(u'bagni_image', 'name_it')

        # Deleting field 'Image.slug_en'
        db.delete_column(u'bagni_image', 'slug_en')

        # Deleting field 'Image.slug_it'
        db.delete_column(u'bagni_image', 'slug_it')


    models = {
        u'bagni.bagno': {
            'Meta': {'object_name': 'Bagno'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address_it': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '125', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'city_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'city_it': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'description_en': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'description_it': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '125', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bagni.Service']", 'symmetrical': 'False', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '75', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'slug_en': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_it': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '125', 'blank': 'True'}),
            'winter_tel': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'})
        },
        u'bagni.image': {
            'Meta': {'object_name': 'Image'},
            'bagno': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bagni.Bagno']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'slug_en': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_it': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'bagni.service': {
            'Meta': {'object_name': 'Service'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'NS'", 'max_length': '50', 'blank': 'True'}),
            'free': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name_it': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'slug_en': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug_it': ('autoslug.fields.AutoSlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bagni']