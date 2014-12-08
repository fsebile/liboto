# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=160)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn', models.BigIntegerField()),
                ('title', models.CharField(max_length=160)),
                ('year', models.DateField()),
                ('cover_image', models.URLField(null=True, blank=True)),
                ('type', models.CharField(max_length=1, choices=[(b'b', b'Book'), (b'm', b'Magazine'), (b'n', b'Newspaper')])),
                ('author', models.ForeignKey(to='main.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=160)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='media',
            name='publisher',
            field=models.ForeignKey(to='main.Publisher'),
            preserve_default=True,
        ),
    ]
