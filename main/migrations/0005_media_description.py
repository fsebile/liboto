# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20141215_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='description',
            field=models.CharField(default=b'-', max_length=320),
            preserve_default=True,
        ),
    ]
