# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PageContentType'
        db.create_table(u'pages_pagecontenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('class_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('admin_class_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('is_extended', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pages', ['PageContentType'])

        # Adding model 'PageSlugContent'
        db.create_table(u'pages_pageslugcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5)),
            ('sid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, blank=True)),
            ('is_extended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pageslugcontent_creator', null=True, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pageslugcontent_editor', null=True, to=orm['auth.User'])),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=245)),
        ))
        db.send_create_signal(u'pages', ['PageSlugContent'])

        # Adding unique constraint on 'PageSlugContent', fields ['language', 'page']
        db.create_unique(u'pages_pageslugcontent', ['language', 'page_id'])

        # Adding model 'PageRedirectContent'
        db.create_table(u'pages_pageredirectcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5)),
            ('sid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, blank=True)),
            ('is_extended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pageredirectcontent_creator', null=True, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pageredirectcontent_editor', null=True, to=orm['auth.User'])),
            ('redirect_to_page', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('redirect_to_url', self.gf('django.db.models.fields.URLField')(max_length=254, null=True, blank=True)),
            ('is_permanent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pages', ['PageRedirectContent'])

        # Adding model 'PageMetaContent'
        db.create_table(u'pages_pagemetacontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5)),
            ('sid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, blank=True)),
            ('is_extended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pagemetacontent_creator', null=True, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pagemetacontent_editor', null=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=160, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=160, blank=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('is_noindex', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_nofollow', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pages', ['PageMetaContent'])

        # Adding unique constraint on 'PageMetaContent', fields ['language', 'page']
        db.create_unique(u'pages_pagemetacontent', ['language', 'page_id'])

        # Adding model 'PageTextContent'
        db.create_table(u'pages_pagetextcontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5)),
            ('sid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, blank=True)),
            ('is_extended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pagetextcontent_creator', null=True, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pagetextcontent_editor', null=True, to=orm['auth.User'])),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_template', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pages', ['PageTextContent'])

        # Adding model 'PageMarkdownContent'
        db.create_table(u'pages_pagemarkdowncontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5)),
            ('sid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, blank=True)),
            ('is_extended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pagemarkdowncontent_creator', null=True, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pagemarkdowncontent_editor', null=True, to=orm['auth.User'])),
            ('text', self.gf('markitup.fields.MarkupField')(no_rendered_field=True, blank=True)),
            ('is_template', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'_text_rendered', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'pages', ['PageMarkdownContent'])

        # Adding model 'PageImageContent'
        db.create_table(u'pages_pageimagecontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'])),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=5)),
            ('sid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, blank=True)),
            ('is_extended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pageimagecontent_creator', null=True, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'pages_pageimagecontent_editor', null=True, to=orm['auth.User'])),
            ('image', self.gf(u'django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('cropping', self.gf(u'django.db.models.fields.CharField')(default=u'', max_length=255, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal(u'pages', ['PageImageContent'])

        # Adding model 'Page'
        db.create_table(u'pages_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name=u'children', null=True, to=orm['pages.Page'])),
            ('template', self.gf('django.db.models.fields.CharField')(max_length=254, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=254, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'page_creator', null=True, to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'page_editor', null=True, to=orm['auth.User'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_approved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_publication', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_publication_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_draft', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_login_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_permission_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'pages', ['Page'])

        # Adding M2M table for field sites on 'Page'
        m2m_table_name = db.shorten_name(u'pages_page_sites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm[u'pages.page'], null=False)),
            ('site', models.ForeignKey(orm[u'sites.site'], null=False))
        ))
        db.create_unique(m2m_table_name, ['page_id', 'site_id'])

        # Adding model 'PageUserObjectPermission'
        db.create_table(u'pages_pageuserobjectpermission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('permission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Permission'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'])),
        ))
        db.send_create_signal(u'pages', ['PageUserObjectPermission'])

        # Adding model 'PageGroupObjectPermission'
        db.create_table(u'pages_pagegroupobjectpermission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('permission', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Permission'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.Group'])),
            ('content_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'])),
        ))
        db.send_create_signal(u'pages', ['PageGroupObjectPermission'])

        # Adding model 'PageContent'
        db.create_table(u'pages_pagecontent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.PageContentType'])),
        ))
        db.send_create_signal(u'pages', ['PageContent'])

        # Adding unique constraint on 'PageContent', fields ['page', 'type']
        db.create_unique(u'pages_pagecontent', ['page_id', 'type_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'PageContent', fields ['page', 'type']
        db.delete_unique(u'pages_pagecontent', ['page_id', 'type_id'])

        # Removing unique constraint on 'PageMetaContent', fields ['language', 'page']
        db.delete_unique(u'pages_pagemetacontent', ['language', 'page_id'])

        # Removing unique constraint on 'PageSlugContent', fields ['language', 'page']
        db.delete_unique(u'pages_pageslugcontent', ['language', 'page_id'])

        # Deleting model 'PageContentType'
        db.delete_table(u'pages_pagecontenttype')

        # Deleting model 'PageSlugContent'
        db.delete_table(u'pages_pageslugcontent')

        # Deleting model 'PageRedirectContent'
        db.delete_table(u'pages_pageredirectcontent')

        # Deleting model 'PageMetaContent'
        db.delete_table(u'pages_pagemetacontent')

        # Deleting model 'PageTextContent'
        db.delete_table(u'pages_pagetextcontent')

        # Deleting model 'PageMarkdownContent'
        db.delete_table(u'pages_pagemarkdowncontent')

        # Deleting model 'PageImageContent'
        db.delete_table(u'pages_pageimagecontent')

        # Deleting model 'Page'
        db.delete_table(u'pages_page')

        # Removing M2M table for field sites on 'Page'
        db.delete_table(db.shorten_name(u'pages_page_sites'))

        # Deleting model 'PageUserObjectPermission'
        db.delete_table(u'pages_pageuserobjectpermission')

        # Deleting model 'PageGroupObjectPermission'
        db.delete_table(u'pages_pagegroupobjectpermission')

        # Deleting model 'PageContent'
        db.delete_table(u'pages_pagecontent')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pages.page': {
            'Meta': {'ordering': "[u'tree_id', u'lft']", 'object_name': 'Page'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '254', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'page_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'date_approved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_publication': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_publication_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_login_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_permission_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['pages.Page']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'template': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'page_editor'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'pages.pagecontent': {
            'Meta': {'unique_together': "((u'page', u'type'),)", 'object_name': 'PageContent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.Page']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.PageContentType']"})
        },
        u'pages.pagecontenttype': {
            'Meta': {'object_name': 'PageContentType'},
            'admin_class_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_extended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pages.pagegroupobjectpermission': {
            'Meta': {'object_name': 'PageGroupObjectPermission'},
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.Page']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Permission']"})
        },
        u'pages.pageimagecontent': {
            'Meta': {'object_name': 'PageImageContent'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pageimagecontent_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'cropping': (u'django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': (u'django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_extended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.Page']"}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pageimagecontent_editor'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'pages.pagemarkdowncontent': {
            'Meta': {'object_name': 'PageMarkdownContent'},
            u'_text_rendered': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pagemarkdowncontent_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_extended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.Page']"}),
            'text': ('markitup.fields.MarkupField', [], {u'no_rendered_field': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pagemarkdowncontent_editor'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'pages.pagemetacontent': {
            'Meta': {'unique_together': "((u'language', u'page'),)", 'object_name': 'PageMetaContent'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pagemetacontent_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '160', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_extended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_nofollow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_noindex': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.Page']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '160', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pagemetacontent_editor'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'pages.pageredirectcontent': {
            'Meta': {'object_name': 'PageRedirectContent'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pageredirectcontent_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_extended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_permanent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.Page']"}),
            'redirect_to_page': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'redirect_to_url': ('django.db.models.fields.URLField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pageredirectcontent_editor'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'pages.pageslugcontent': {
            'Meta': {'unique_together': "((u'language', u'page'),)", 'object_name': 'PageSlugContent'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pageslugcontent_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_extended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.Page']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '245'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pageslugcontent_editor'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'pages.pagetextcontent': {
            'Meta': {'object_name': 'PageTextContent'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pagetextcontent_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_extended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.Page']"}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'pages_pagetextcontent_editor'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'pages.pageuserobjectpermission': {
            'Meta': {'object_name': 'PageUserObjectPermission'},
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pages.Page']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Permission']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['pages']
