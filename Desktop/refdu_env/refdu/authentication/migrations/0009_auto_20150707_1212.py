# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20150707_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('token', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Person1',
            new_name='Person',
        ),
        migrations.RemoveField(
            model_name='token1',
            name='user',
        ),
        migrations.DeleteModel(
            name='Token1',
        ),
        migrations.AddField(
            model_name='token',
            name='user',
            field=models.ForeignKey(to='authentication.Person'),
            preserve_default=True,
        ),
    ]
