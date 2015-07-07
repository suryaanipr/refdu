# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20150706_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('token', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to='authentication.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
