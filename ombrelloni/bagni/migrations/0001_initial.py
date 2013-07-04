# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Bagno'
        db.create_table(u'bagni_bagno', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from='name')),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('mail', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('site', self.gf('django.db.models.fields.URLField')(max_length=50, blank=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True, null=True)),
        ))
        db.send_create_signal(u'bagni', ['Bagno'])

        # Adding M2M table for field services on 'Bagno'
        m2m_table_name = db.shorten_name(u'bagni_bagno_services')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bagno', models.ForeignKey(orm[u'bagni.bagno'], null=False)),
            ('service', models.ForeignKey(orm[u'bagni.service'], null=False))
        ))
        db.create_unique(m2m_table_name, ['bagno_id', 'service_id'])

        # Adding model 'Service'
        db.create_table(u'bagni_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from='name')),
            ('category', self.gf('django.db.models.fields.CharField')(default='OT', max_length=50, blank=True)),
            ('free', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'bagni', ['Service'])


    def backwards(self, orm):
        # Deleting model 'Bagno'
        db.delete_table(u'bagni_bagno')

        # Removing M2M table for field services on 'Bagno'
        db.delete_table(db.shorten_name(u'bagni_bagno_services'))

        # Deleting model 'Service'
        db.delete_table(u'bagni_service')


    models = {
        u'bagni.bagno': {
            'Meta': {'object_name': 'Bagno'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['bagni.Service']", 'symmetrical': 'False', 'blank': 'True'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '50', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'bagni.service': {
            'Meta': {'object_name': 'Service'},
            'category': ('django.db.models.fields.CharField', [], {'default': "'OT'", 'max_length': '50', 'blank': 'True'}),
            'free': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'name'"})
        }
    }

    complete_apps = ['bagni']
