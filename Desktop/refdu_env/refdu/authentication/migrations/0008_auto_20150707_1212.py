# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token1',
            fields=[
                ('token', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Person',
            new_name='Person1',
        ),
        migrations.RemoveField(
            model_name='token',
            name='user',
        ),
        migrations.DeleteModel(
            name='Token',
        ),
        migrations.AddField(
            model_name='token1',
            name='user',
            field=models.ForeignKey(to='authentication.Person1'),
            preserve_default=True,
        ),
    ]
