
from south.db import db
from django.db import models
from urlweb.shortener.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Link'
        db.create_table('shortener_link', (
            ('id', orm['shortener.Link:id']),
            ('user', orm['shortener.Link:user']),
            ('url', orm['shortener.Link:url']),
            ('date_submitted', orm['shortener.Link:date_submitted']),
            ('main_url', orm['shortener.Link:main_url']),
        ))
        db.send_create_signal('shortener', ['Link'])
        
        # Adding model 'Stat'
        db.create_table('shortener_stat', (
            ('id', orm['shortener.Stat:id']),
            ('link', orm['shortener.Stat:link']),
            ('user', orm['shortener.Stat:user']),
            ('http_host', orm['shortener.Stat:http_host']),
            ('http_referer', orm['shortener.Stat:http_referer']),
            ('http_user_agent', orm['shortener.Stat:http_user_agent']),
            ('remote_addr', orm['shortener.Stat:remote_addr']),
            ('remote_host', orm['shortener.Stat:remote_host']),
            ('date', orm['shortener.Stat:date']),
        ))
        db.send_create_signal('shortener', ['Stat'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Link'
        db.delete_table('shortener_link')
        
        # Deleting model 'Stat'
        db.delete_table('shortener_stat')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'shortener.link': {
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 11, 18, 15, 15, 32, 430972)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_url': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rollup'", 'null': 'True', 'to': "orm['shortener.Link']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']"})
        },
        'shortener.stat': {
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2009, 11, 18, 15, 15, 32, 431945)'}),
            'http_host': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'http_referer': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'http_user_agent': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['shortener.Link']"}),
            'remote_addr': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'remote_host': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['auth.User']"})
        }
    }
    
    complete_apps = ['shortener']
