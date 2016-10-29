# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageDefaultContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('content_types', models.CharField(max_length=254)),
            ],
            options={
                'verbose_name': 'Default Content',
                'verbose_name_plural': 'Default Content',
            },
        ),
        migrations.AddField(
            model_name='page',
            name='default_content',
            field=models.ForeignKey(related_name='page_default_content', to='pages.PageDefaultContent', null=True),
        ),
    ]
