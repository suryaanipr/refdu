# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_person_isactive'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='activate_token',
            field=models.CharField(default=b' ', max_length=250),
            preserve_default=True,
        ),
    ]
