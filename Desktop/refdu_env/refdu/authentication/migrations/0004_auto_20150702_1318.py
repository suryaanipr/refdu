# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20150702_1312'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User_Details',
            new_name='Person',
        ),
    ]
