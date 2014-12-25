# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='isbn',
            field=models.CharField(max_length=13),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='media',
            name='type',
            field=models.CharField(default=b'b', max_length=1, choices=[(b'b', b'Book'), (b'm', b'Magazine'), (b'n', b'Newspaper')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='media',
            name='year',
            field=models.CharField(max_length=4),
            preserve_default=True,
        ),
    ]
