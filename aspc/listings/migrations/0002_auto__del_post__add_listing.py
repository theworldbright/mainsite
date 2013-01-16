# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Post'
        db.delete_table('listings_post')

        # Adding model 'Listing'
        db.create_table('listings_listing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('price', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('listings', ['Listing'])

    def backwards(self, orm):
        # Adding model 'Post'
        db.create_table('listings_post', (
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('price', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('listings', ['Post'])

        # Deleting model 'Listing'
        db.delete_table('listings_listing')

    models = {
        'listings.listing': {
            'Meta': {'object_name': 'Listing'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        }
    }

    complete_apps = ['listings']