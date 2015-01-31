# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields
import django.utils.timezone
import pages.storage
from django.conf import settings
import markitup.fields
import mptt.fields
import pages.models.pagecontenttypes


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('template', models.CharField(max_length=254, blank=True)),
                ('comment', models.TextField(max_length=254, blank=True)),
                ('date_created', models.DateTimeField(verbose_name='Created', default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(verbose_name='Updated', default=django.utils.timezone.now)),
                ('date_approved', models.DateTimeField(verbose_name='Approved', null=True, blank=True)),
                ('date_publication', models.DateTimeField(verbose_name='Publication date', null=True, blank=True)),
                ('date_publication_end', models.DateTimeField(verbose_name='Publication end date', null=True, blank=True)),
                ('is_draft', models.BooleanField(verbose_name='Draft', default=True)),
                ('is_approved', models.BooleanField(verbose_name='Approved', default=False)),
                ('is_hidden', models.BooleanField(verbose_name='Hidden', default=False)),
                ('is_published', models.BooleanField(verbose_name='Published', default=False)),
                ('is_login_required', models.BooleanField(verbose_name='Login required', default=False)),
                ('is_permission_required', models.BooleanField(verbose_name='Permission required', default=False)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('created_by', models.ForeignKey(related_name='page_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='pages.Page', null=True)),
                ('sites', models.ManyToManyField(verbose_name='sites', to='sites.Site', help_text='The site(s) where this pages is accessible.')),
                ('updated_by', models.ForeignKey(related_name='page_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Page',
                'permissions': (('view_page', 'Can view pages'),),
                'verbose_name_plural': 'Pages',
                'ordering': ['tree_id', 'lft'],
                'get_latest_by': 'date_publication',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Content',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('type', models.CharField(verbose_name='Type', max_length=100)),
                ('class_name', models.CharField(verbose_name='Class', max_length=100)),
                ('admin_class_name', models.CharField(verbose_name='Admin Class', max_length=100)),
                ('is_extended', models.BooleanField(verbose_name='Extended', default=False)),
            ],
            options={
                'verbose_name': 'Content Type',
                'verbose_name_plural': 'Content Types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageGroupObjectPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('content_object', models.ForeignKey(to='pages.Page')),
                ('group', models.ForeignKey(to='auth.Group')),
                ('permission', models.ForeignKey(to='auth.Permission')),
            ],
            options={
                'verbose_name': 'Page Group Permissions',
                'verbose_name_plural': 'Pages Groups Permissions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageImageContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('type', models.CharField(verbose_name='Type', max_length=100, db_index=True)),
                ('language', models.CharField(default='en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(verbose_name='Extended?', default=False)),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(verbose_name='Created', default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(verbose_name='Updated', default=django.utils.timezone.now)),
                ('image', image_cropping.fields.ImageCropField(null=True, storage=pages.storage.PageFileSystemStorage(), upload_to=pages.models.pagecontenttypes.make_image_upload_path, blank=True)),
                ('cropping', image_cropping.fields.ImageRatioField('image', '600x800', hide_image_field=False, verbose_name='cropping', free_crop=False, allow_fullsize=True, adapt_rotation=False, size_warning=True, help_text=None)),
                ('title', models.CharField(max_length=250, blank=True)),
                ('tags', models.CharField(max_length=250, blank=True)),
                ('created_by', models.ForeignKey(related_name='pages_pageimagecontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='pages_pageimagecontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageMarkdownContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('type', models.CharField(verbose_name='Type', max_length=100, db_index=True)),
                ('language', models.CharField(default='en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(verbose_name='Extended?', default=False)),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(verbose_name='Created', default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(verbose_name='Updated', default=django.utils.timezone.now)),
                ('text', markitup.fields.MarkupField(no_rendered_field=True, blank=True)),
                ('is_template', models.BooleanField(verbose_name='Template?', default=False)),
                ('_text_rendered', models.TextField(editable=False, blank=True)),
                ('created_by', models.ForeignKey(related_name='pages_pagemarkdowncontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='pages_pagemarkdowncontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Markdown',
                'verbose_name_plural': 'Markdown',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageMetaContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('type', models.CharField(verbose_name='Type', max_length=100, db_index=True)),
                ('language', models.CharField(default='en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(verbose_name='Extended?', default=False)),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(verbose_name='Created', default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(verbose_name='Updated', default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=160, blank=True)),
                ('description', models.TextField(max_length=160, blank=True)),
                ('keywords', models.CharField(max_length=200, blank=True)),
                ('is_noindex', models.BooleanField(verbose_name='NoIndex', default=False)),
                ('is_nofollow', models.BooleanField(verbose_name='NoFollow', default=False)),
                ('created_by', models.ForeignKey(related_name='pages_pagemetacontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='pages_pagemetacontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Meta',
                'verbose_name_plural': 'Meta',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageRedirectContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('type', models.CharField(verbose_name='Type', max_length=100, db_index=True)),
                ('language', models.CharField(default='en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(verbose_name='Extended?', default=False)),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(verbose_name='Created', default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(verbose_name='Updated', default=django.utils.timezone.now)),
                ('redirect_to_page', models.CharField(null=True, max_length=254, blank=True)),
                ('redirect_to_url', models.URLField(null=True, max_length=254, blank=True)),
                ('is_permanent', models.BooleanField(verbose_name='Permanent', default=False)),
                ('created_by', models.ForeignKey(related_name='pages_pageredirectcontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='pages_pageredirectcontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Redirect',
                'verbose_name_plural': 'Redirect',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageSlugContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('type', models.CharField(verbose_name='Type', max_length=100, db_index=True)),
                ('language', models.CharField(default='en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(verbose_name='Extended?', default=False)),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(verbose_name='Created', default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(verbose_name='Updated', default=django.utils.timezone.now)),
                ('slug', models.CharField(max_length=245)),
                ('created_by', models.ForeignKey(related_name='pages_pageslugcontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='pages_pageslugcontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Slug',
                'verbose_name_plural': 'Slugs',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageTextContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('type', models.CharField(verbose_name='Type', max_length=100, db_index=True)),
                ('language', models.CharField(default='en', max_length=5)),
                ('sid', models.CharField(unique=True, max_length=200)),
                ('name', models.CharField(unique=True, max_length=200, blank=True)),
                ('is_extended', models.BooleanField(verbose_name='Extended?', default=False)),
                ('comment', models.CharField(max_length=250, blank=True)),
                ('date_created', models.DateTimeField(verbose_name='Created', default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(verbose_name='Updated', default=django.utils.timezone.now)),
                ('text', models.TextField(blank=True)),
                ('is_template', models.BooleanField(verbose_name='Template?', default=False)),
                ('created_by', models.ForeignKey(related_name='pages_pagetextcontent_creator', to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(verbose_name='Page', to='pages.Page')),
                ('updated_by', models.ForeignKey(related_name='pages_pagetextcontent_editor', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Text',
                'verbose_name_plural': 'Text',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageUserObjectPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('content_object', models.ForeignKey(to='pages.Page')),
                ('permission', models.ForeignKey(to='auth.Permission')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Page User Permissions',
                'verbose_name_plural': 'Pages Users Permissions',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='pageslugcontent',
            unique_together=set([('language', 'page')]),
        ),
        migrations.AlterUniqueTogether(
            name='pagemetacontent',
            unique_together=set([('language', 'page')]),
        ),
        migrations.AddField(
            model_name='pagecontent',
            name='type',
            field=models.ForeignKey(to='pages.PageContentType'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='pagecontent',
            unique_together=set([('page', 'type')]),
        ),
    ]
