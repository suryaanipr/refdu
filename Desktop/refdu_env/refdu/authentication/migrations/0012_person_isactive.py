# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_auto_20150708_0820'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='isActive',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
