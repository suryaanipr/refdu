# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20150702_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='person',
            name='password',
            field=models.CharField(default=b' ', max_length=250),
        ),
        migrations.AlterField(
            model_name='person',
            name='role',
            field=models.CharField(default=b' ', max_length=200, choices=[(b'ad', b'Admin'), (b'Cu', b'Customer'), (b'Co', b'Company')]),
        ),
    ]
