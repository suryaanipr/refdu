# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20150702_1306'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Person',
            new_name='User_Details',
        ),
    ]
