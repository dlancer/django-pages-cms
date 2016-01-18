# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import markitup.fields
import mptt.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('ptype', models.CharField(default='page', max_length=64, verbose_name='Type')),
                ('template', models.CharField(max_length=254, blank=True)),
                ('comment', models.TextField(max_length=254, blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created')),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated')),
                ('date_approved', models.DateTimeField(null=True, verbose_name='Approved', blank=True)),
                ('date_publication', models.DateTimeField(null=True, verbose_name='Publication date', blank=True)),
                ('date_publication_end', models.DateTimeField(null=True, verbose_name='Publication end date', blank=True)),
                ('is_draft', models.BooleanField(default=True, verbose_name='Draft')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Approved')),
                ('is_hidden', models.BooleanField(default=False, verbose_name='Hidden')),
                ('is_published', models.BooleanField(default=False, verbose_name='Published')),
                ('is_login_required', models.BooleanField(default=False, verbose_name='Login required')),
                ('is_permission_required', models.BooleanField(default=False, verbose_name='Permission required')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('created_by', models.ForeignKey(related_name='page_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='pages.Page', null=True)),
                ('sites', models.ManyToManyField(help_text='The site(s) where this pages is accessible.', to='sites.Site', verbose_name='sites')),
                ('updated_by', models.ForeignKey(related_name='page_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'get_latest_by': 'date_publication',
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'permissions': (('view_page', 'Can view pages'),),
            },
        ),
        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Content',
            },
        ),
        migrations.CreateModel(
            name='PageContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='Type')),
                ('class_name', models.CharField(max_length=100, verbose_name='Class')),
                ('admin_class_name', models.CharField(max_length=100, verbose_name='Admin Class')),
                ('is_extended', models.BooleanField(default=False, verbose_name='Extended')),
            ],
            options={
                'verbose_name': 'Content Type',
                'verbose_name_plural': 'Content Types',
            },
        ),
        migrations.CreateModel(
            name='PageGroupObjectPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', models.ForeignKey(to='pages.Page')),
                ('group', models.ForeignKey(to='auth.Group')),
                ('permission', models.ForeignKey(to='auth.Permission')),
            ],
            options={
                'verbose_name': 'Page Group Permissions',
                'verbose_name_plural': 'Pages Groups Permissions',
            },
        ),
        migrations.CreateModel(
            name='PageMarkdownContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='Type', db_index=True)),
                ('language', models.CharField(default=b'en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(default=False, verbose_name='Extended?')),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created')),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated')),
                ('text', markitup.fields.MarkupField(no_rendered_field=True, blank=True)),
                ('is_template', models.BooleanField(default=False, verbose_name='Template?')),
                ('_text_rendered', models.TextField(editable=False, blank=True)),
                ('created_by', models.ForeignKey(related_name='pages_pagemarkdowncontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='pages_pagemarkdowncontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Markdown',
                'verbose_name_plural': 'Markdown',
            },
        ),
        migrations.CreateModel(
            name='PageMetaContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='Type', db_index=True)),
                ('language', models.CharField(default=b'en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(default=False, verbose_name='Extended?')),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created')),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated')),
                ('title', models.CharField(max_length=160, blank=True)),
                ('description', models.TextField(max_length=160, blank=True)),
                ('keywords', models.CharField(max_length=200, blank=True)),
                ('is_noindex', models.BooleanField(default=False, verbose_name='NoIndex')),
                ('is_nofollow', models.BooleanField(default=False, verbose_name='NoFollow')),
                ('created_by', models.ForeignKey(related_name='pages_pagemetacontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='pages_pagemetacontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Meta',
                'verbose_name_plural': 'Meta',
            },
        ),
        migrations.CreateModel(
            name='PageRedirectContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='Type', db_index=True)),
                ('language', models.CharField(default=b'en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(default=False, verbose_name='Extended?')),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created')),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated')),
                ('redirect_to_page', models.CharField(max_length=254, null=True, blank=True)),
                ('redirect_to_url', models.URLField(max_length=254, null=True, blank=True)),
                ('is_permanent', models.BooleanField(default=False, verbose_name='Permanent')),
                ('created_by', models.ForeignKey(related_name='pages_pageredirectcontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='pages_pageredirectcontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Redirect',
                'verbose_name_plural': 'Redirect',
            },
        ),
        migrations.CreateModel(
            name='PageSlugContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='Type', db_index=True)),
                ('language', models.CharField(default=b'en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(default=False, verbose_name='Extended?')),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created')),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated')),
                ('slug', models.CharField(max_length=245)),
                ('created_by', models.ForeignKey(related_name='pages_pageslugcontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='pages_pageslugcontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Slug',
                'verbose_name_plural': 'Slugs',
            },
        ),
        migrations.CreateModel(
            name='PageTextContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='Type', db_index=True)),
                ('language', models.CharField(default=b'en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(default=False, verbose_name='Extended?')),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created')),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated')),
                ('text', models.TextField(blank=True)),
                ('is_template', models.BooleanField(default=False, verbose_name='Template?')),
                ('created_by', models.ForeignKey(related_name='pages_pagetextcontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='pages_pagetextcontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Text',
                'verbose_name_plural': 'Text',
            },
        ),
        migrations.CreateModel(
            name='PageUserObjectPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_object', models.ForeignKey(to='pages.Page')),
                ('permission', models.ForeignKey(to='auth.Permission')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Page User Permissions',
                'verbose_name_plural': 'Pages Users Permissions',
            },
        ),
        migrations.AddField(
            model_name='pagecontent',
            name='type',
            field=models.ForeignKey(to='pages.PageContentType'),
        ),
        migrations.AlterUniqueTogether(
            name='pageslugcontent',
            unique_together=set([('language', 'page')]),
        ),
        migrations.AlterUniqueTogether(
            name='pagemetacontent',
            unique_together=set([('language', 'page')]),
        ),
        migrations.AlterUniqueTogether(
            name='pagecontent',
            unique_together=set([('page', 'type')]),
        ),
    ]
